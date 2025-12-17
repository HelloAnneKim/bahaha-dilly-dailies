import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# Page config
st.set_page_config(
    page_title="Bahaha Dilly Dailies",
    page_icon="🏆",
    layout="wide"
)

# Connect to Google Sheets
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def load_data():
    """Load data from Google Sheets"""
    try:
        conn = get_connection()
        df = conn.read(ttl="0")  # ttl=0 means always fetch fresh data

        # If sheet is empty, return empty DataFrame with correct columns
        if df.empty:
            return pd.DataFrame(columns=['user', 'date', 'sleep', 'exercise', 'pt_quota', 'water', 'protein', 'notes', 'timestamp'])

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=['user', 'date', 'sleep', 'exercise', 'pt_quota', 'water', 'protein', 'notes', 'timestamp'])

def save_data(df):
    """Save data to Google Sheets"""
    try:
        conn = get_connection()
        conn.update(data=df)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Load data
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# App title
st.title("🏆 Bahaha Dilly Dailies")
st.markdown("### Track your daily KPIs and compete with friends!")

# Sidebar for user selection
st.sidebar.title("User Login")
users = ["anne", "bobby", "hansa"]
selected_user = st.sidebar.selectbox("Select your name:", users)

st.sidebar.markdown("---")
st.sidebar.markdown("### KPI Targets")
st.sidebar.markdown("""
- 💤 Sleep: ≥8 hours
- 🏃 Exercise: Daily goal
- 💪 PT Quota: Daily goal
- 💧 Water: Track oz
- 🥩 Protein: Track grams
""")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Log Today", "📊 My Progress", "🏆 Leaderboard", "📈 Analytics"])

# Tab 1: Log Today's KPIs
with tab1:
    st.header(f"Log KPIs for {selected_user}")

    today = str(date.today())

    # Check if already logged today
    user_data = st.session_state.df[
        (st.session_state.df['user'] == selected_user) &
        (st.session_state.df['date'] == today)
    ]
    already_logged = not user_data.empty

    if already_logged:
        st.warning(f"You already logged data for {today}. You can update it below.")
        existing_data = user_data.iloc[0].to_dict()
    else:
        existing_data = {}

    with st.form("kpi_form"):
        st.subheader("Enter your daily metrics:")

        col1, col2 = st.columns(2)

        with col1:
            sleep_hours = st.number_input(
                "💤 Sleep (hours)",
                min_value=0.0,
                max_value=24.0,
                value=float(existing_data.get('sleep', 0.0)),
                step=0.5,
                help="Aim for at least 8 hours"
            )

            exercise_done = st.checkbox(
                "🏃 Completed Exercise",
                value=bool(existing_data.get('exercise', False))
            )

            pt_done = st.checkbox(
                "💪 Completed PT Quota",
                value=bool(existing_data.get('pt_quota', False))
            )

        with col2:
            water_oz = st.number_input(
                "💧 Water (oz)",
                min_value=0,
                max_value=300,
                value=int(existing_data.get('water', 0)),
                step=8,
                help="Track your water intake in ounces"
            )

            protein_g = st.number_input(
                "🥩 Protein (grams)",
                min_value=0,
                max_value=500,
                value=int(existing_data.get('protein', 0)),
                step=10,
                help="Track your protein intake"
            )

        notes = st.text_area(
            "📝 Notes (optional)",
            value=existing_data.get('notes', ''),
            placeholder="Any additional notes about your day..."
        )

        submitted = st.form_submit_button("💾 Save Today's Data", use_container_width=True)

        if submitted:
            # Create new row
            new_row = pd.DataFrame([{
                'user': selected_user,
                'date': today,
                'sleep': sleep_hours,
                'exercise': exercise_done,
                'pt_quota': pt_done,
                'water': water_oz,
                'protein': protein_g,
                'notes': notes,
                'timestamp': datetime.now().isoformat()
            }])

            # Remove old entry if updating
            if already_logged:
                st.session_state.df = st.session_state.df[
                    ~((st.session_state.df['user'] == selected_user) &
                      (st.session_state.df['date'] == today))
                ]

            # Add new row
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

            # Save to Google Sheets
            if save_data(st.session_state.df):
                st.success("✅ Data saved successfully!")
                st.balloons()
            else:
                st.error("Failed to save to Google Sheets")

# Tab 2: My Progress
with tab2:
    st.header(f"{selected_user}'s Progress")

    user_df = st.session_state.df[st.session_state.df['user'] == selected_user].copy()

    if not user_df.empty:
        user_df['date'] = pd.to_datetime(user_df['date'])
        user_df = user_df.sort_values('date')

        # Summary metrics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            avg_sleep = user_df['sleep'].mean()
            st.metric("Avg Sleep", f"{avg_sleep:.1f}h",
                     delta=f"{avg_sleep - 8:.1f}h" if avg_sleep >= 8 else f"{avg_sleep - 8:.1f}h")

        with col2:
            exercise_pct = (user_df['exercise'].sum() / len(user_df)) * 100
            st.metric("Exercise Rate", f"{exercise_pct:.0f}%")

        with col3:
            pt_pct = (user_df['pt_quota'].sum() / len(user_df)) * 100
            st.metric("PT Rate", f"{pt_pct:.0f}%")

        with col4:
            avg_water = user_df['water'].mean()
            st.metric("Avg Water", f"{avg_water:.0f}oz")

        with col5:
            avg_protein = user_df['protein'].mean()
            st.metric("Avg Protein", f"{avg_protein:.0f}g")

        # Charts
        st.subheader("📈 Trends")

        # Sleep trend
        fig_sleep = px.line(user_df, x='date', y='sleep', title='Sleep Trend',
                           labels={'sleep': 'Hours', 'date': 'Date'})
        fig_sleep.add_hline(y=8, line_dash="dash", line_color="green",
                           annotation_text="Target: 8h")
        st.plotly_chart(fig_sleep, use_container_width=True)

        # Water and Protein
        col1, col2 = st.columns(2)

        with col1:
            fig_water = px.bar(user_df, x='date', y='water', title='Water Intake',
                              labels={'water': 'Ounces', 'date': 'Date'})
            st.plotly_chart(fig_water, use_container_width=True)

        with col2:
            fig_protein = px.bar(user_df, x='date', y='protein', title='Protein Intake',
                                labels={'protein': 'Grams', 'date': 'Date'})
            st.plotly_chart(fig_protein, use_container_width=True)

        # Recent entries
        st.subheader("📅 Recent Entries")
        display_df = user_df[['date', 'sleep', 'exercise', 'pt_quota', 'water', 'protein']].tail(10)
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_df, use_container_width=True)

    else:
        st.info("No data logged yet. Go to 'Log Today' to start tracking!")

# Tab 3: Leaderboard
with tab3:
    st.header("🏆 Leaderboard")

    if not st.session_state.df.empty:
        leaderboard_data = []

        for user in users:
            user_df = st.session_state.df[st.session_state.df['user'] == user]

            if user_df.empty:
                continue

            total_days = len(user_df)
            sleep_score = (user_df['sleep'] >= 8).sum()
            exercise_score = user_df['exercise'].sum()
            pt_score = user_df['pt_quota'].sum()
            avg_water = user_df['water'].mean()
            avg_protein = user_df['protein'].mean()

            # Overall score (weighted)
            overall_score = (
                sleep_score * 10 +
                exercise_score * 15 +
                pt_score * 15 +
                (avg_water / 10) +
                (avg_protein / 10)
            )

            leaderboard_data.append({
                'User': user,
                'Total Days': total_days,
                'Sleep Goals Met': int(sleep_score),
                'Exercise Days': int(exercise_score),
                'PT Days': int(pt_score),
                'Avg Water (oz)': f"{avg_water:.0f}",
                'Avg Protein (g)': f"{avg_protein:.0f}",
                'Overall Score': overall_score
            })

        # Create leaderboard DataFrame
        lb_df = pd.DataFrame(leaderboard_data)
        lb_df = lb_df.sort_values('Overall Score', ascending=False).reset_index(drop=True)
        lb_df.index = lb_df.index + 1

        # Display podium
        if len(lb_df) >= 1:
            cols = st.columns(len(lb_df))
            medals = ['🥇', '🥈', '🥉']

            for idx, (i, row) in enumerate(lb_df.iterrows()):
                with cols[idx]:
                    medal = medals[idx] if idx < 3 else '🏅'
                    st.markdown(f"### {medal} #{i}")
                    st.markdown(f"### {row['User']}")
                    st.metric("Score", f"{row['Overall Score']:.0f}")

        # Detailed leaderboard
        st.subheader("📊 Detailed Rankings")
        st.dataframe(lb_df, use_container_width=True)

        # Competition insights
        st.subheader("🔥 Competition Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            sleep_leader = lb_df.loc[lb_df['Sleep Goals Met'].astype(int).idxmax(), 'User']
            st.info(f"💤 Sleep Champion: **{sleep_leader}**")

        with col2:
            exercise_leader = lb_df.loc[lb_df['Exercise Days'].astype(int).idxmax(), 'User']
            st.info(f"🏃 Exercise Champion: **{exercise_leader}**")

        with col3:
            pt_leader = lb_df.loc[lb_df['PT Days'].astype(int).idxmax(), 'User']
            st.info(f"💪 PT Champion: **{pt_leader}**")

    else:
        st.info("No data available yet. Start logging to see the leaderboard!")

# Tab 4: Analytics
with tab4:
    st.header("📈 Group Analytics")

    if not st.session_state.df.empty:
        df_all = st.session_state.df.copy()

        # Group comparison
        st.subheader("👥 Group Comparison")

        metric_choice = st.selectbox(
            "Select metric to compare:",
            ['sleep', 'water', 'protein']
        )

        fig = px.box(df_all, x='user', y=metric_choice,
                    title=f'{metric_choice.capitalize()} Distribution by User',
                    color='user')
        st.plotly_chart(fig, use_container_width=True)

        # Timeline comparison
        st.subheader("📅 Timeline Comparison")

        df_avg = df_all.groupby(['date', 'user'])[metric_choice].mean().reset_index()
        df_avg['date'] = pd.to_datetime(df_avg['date'])

        fig_timeline = px.line(df_avg, x='date', y=metric_choice,
                              color='user', title=f'{metric_choice.capitalize()} Over Time')
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Success rates
        st.subheader("✅ Success Rates")

        col1, col2 = st.columns(2)

        with col1:
            exercise_rates = df_all.groupby('user')['exercise'].mean() * 100
            fig_ex = px.bar(exercise_rates, title='Exercise Completion Rate',
                           labels={'value': 'Percentage', 'user': 'User'})
            st.plotly_chart(fig_ex, use_container_width=True)

        with col2:
            pt_rates = df_all.groupby('user')['pt_quota'].mean() * 100
            fig_pt = px.bar(pt_rates, title='PT Quota Completion Rate',
                           labels={'value': 'Percentage', 'user': 'User'})
            st.plotly_chart(fig_pt, use_container_width=True)

    else:
        st.info("No data available yet for analytics!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for tracking daily progress | 🏆 Keep grinding!")

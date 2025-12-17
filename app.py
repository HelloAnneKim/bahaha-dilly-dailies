import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Page config
st.set_page_config(
    page_title="Bahaha Dilly Dailies",
    page_icon="🏆",
    layout="wide"
)

# Google Sheets setup
SPREADSHEET_ID = "1XcW5S3flYiSkOBhxCyJ0VuZGWp462Oa8Eah6LnlAU1U"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_google_sheet():
    """Connect to Google Sheets using service account credentials"""
    try:
        # Check if credentials file exists
        creds_file = Path("credentials.json")
        if not creds_file.exists():
            st.error("⚠️ credentials.json not found. Please add your Google service account credentials.")
            st.info("See README.md for setup instructions.")
            return None

        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        return sheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

def load_data():
    """Load data from Google Sheets"""
    sheet = get_google_sheet()
    if sheet is None:
        return {}

    try:
        # Get all records from the sheet
        records = sheet.get_all_records()

        # Convert to nested dictionary format: {user: {date: {metrics}}}
        data = {}
        for record in records:
            user = record.get('user', '')
            date_str = record.get('date', '')

            if user and date_str:
                if user not in data:
                    data[user] = {}

                data[user][date_str] = {
                    'sleep': float(record.get('sleep', 0)),
                    'exercise': record.get('exercise', 'FALSE') == 'TRUE',
                    'pt_quota': record.get('pt_quota', 'FALSE') == 'TRUE',
                    'water': int(record.get('water', 0)),
                    'protein': int(record.get('protein', 0)),
                    'notes': record.get('notes', ''),
                    'timestamp': record.get('timestamp', '')
                }

        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

def save_data(data):
    """Save data to Google Sheets"""
    sheet = get_google_sheet()
    if sheet is None:
        return

    try:
        # Convert nested dictionary to list of rows
        rows = [['user', 'date', 'sleep', 'exercise', 'pt_quota', 'water', 'protein', 'notes', 'timestamp']]

        for user, dates in data.items():
            for date_str, metrics in dates.items():
                rows.append([
                    user,
                    date_str,
                    metrics.get('sleep', 0),
                    'TRUE' if metrics.get('exercise', False) else 'FALSE',
                    'TRUE' if metrics.get('pt_quota', False) else 'FALSE',
                    metrics.get('water', 0),
                    metrics.get('protein', 0),
                    metrics.get('notes', ''),
                    metrics.get('timestamp', '')
                ])

        # Clear existing data and write new data
        sheet.clear()
        sheet.update(values=rows, range_name='A1')

    except Exception as e:
        st.error(f"Error saving data: {e}")

# Load data
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# App title
st.title("🏆 Bahaha Dilly Dailies")
st.markdown("### Track your daily KPIs and compete with friends!")

# Sidebar for user selection
st.sidebar.title("User Login")
users = ["anne", "bobby", "hansa"]
selected_user = st.sidebar.selectbox("Select your name:", users)

# Add custom name option
if st.sidebar.checkbox("Customize names"):
    st.sidebar.info("Edit the 'users' list in app.py to change names")

st.sidebar.markdown("---")
st.sidebar.markdown("### KPI Targets")
st.sidebar.markdown("""
- 💤 Sleep: ≥8 hours
- 🏃 Exercise: Daily goal
- 💪 PT Quota: Daily goal
- 💧 Water: Track oz/liters
- 🥩 Protein: Track grams
""")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Log Today", "📊 My Progress", "🏆 Leaderboard", "📈 Analytics"])

# Tab 1: Log Today's KPIs
with tab1:
    st.header(f"Log KPIs for {selected_user}")

    today = str(date.today())

    # Check if already logged today
    user_data = st.session_state.data.get(selected_user, {})
    already_logged = today in user_data

    if already_logged:
        st.warning(f"You already logged data for {today}. You can update it below.")
        existing_data = user_data[today]
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
                value=existing_data.get('sleep', 0.0),
                step=0.5,
                help="Aim for at least 8 hours"
            )

            exercise_done = st.checkbox(
                "🏃 Completed Exercise",
                value=existing_data.get('exercise', False)
            )

            pt_done = st.checkbox(
                "💪 Completed PT Quota",
                value=existing_data.get('pt_quota', False)
            )

        with col2:
            water_oz = st.number_input(
                "💧 Water (oz)",
                min_value=0,
                max_value=300,
                value=existing_data.get('water', 0),
                step=8,
                help="Track your water intake in ounces"
            )

            protein_g = st.number_input(
                "🥩 Protein (grams)",
                min_value=0,
                max_value=500,
                value=existing_data.get('protein', 0),
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
            # Save data
            if selected_user not in st.session_state.data:
                st.session_state.data[selected_user] = {}

            st.session_state.data[selected_user][today] = {
                'sleep': sleep_hours,
                'exercise': exercise_done,
                'pt_quota': pt_done,
                'water': water_oz,
                'protein': protein_g,
                'notes': notes,
                'timestamp': datetime.now().isoformat()
            }

            save_data(st.session_state.data)
            st.success("✅ Data saved successfully!")
            st.balloons()

# Tab 2: My Progress
with tab2:
    st.header(f"{selected_user}'s Progress")

    if selected_user in st.session_state.data and st.session_state.data[selected_user]:
        user_data = st.session_state.data[selected_user]

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(user_data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # Summary metrics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            avg_sleep = df['sleep'].mean()
            st.metric("Avg Sleep", f"{avg_sleep:.1f}h",
                     delta=f"{avg_sleep - 8:.1f}h" if avg_sleep >= 8 else f"{avg_sleep - 8:.1f}h")

        with col2:
            exercise_pct = (df['exercise'].sum() / len(df)) * 100
            st.metric("Exercise Rate", f"{exercise_pct:.0f}%")

        with col3:
            pt_pct = (df['pt_quota'].sum() / len(df)) * 100
            st.metric("PT Rate", f"{pt_pct:.0f}%")

        with col4:
            avg_water = df['water'].mean()
            st.metric("Avg Water", f"{avg_water:.0f}oz")

        with col5:
            avg_protein = df['protein'].mean()
            st.metric("Avg Protein", f"{avg_protein:.0f}g")

        # Charts
        st.subheader("📈 Trends")

        # Sleep trend
        fig_sleep = px.line(df, y='sleep', title='Sleep Trend',
                           labels={'sleep': 'Hours', 'index': 'Date'})
        fig_sleep.add_hline(y=8, line_dash="dash", line_color="green",
                           annotation_text="Target: 8h")
        st.plotly_chart(fig_sleep, use_container_width=True)

        # Water and Protein
        col1, col2 = st.columns(2)

        with col1:
            fig_water = px.bar(df, y='water', title='Water Intake',
                              labels={'water': 'Ounces', 'index': 'Date'})
            st.plotly_chart(fig_water, use_container_width=True)

        with col2:
            fig_protein = px.bar(df, y='protein', title='Protein Intake',
                                labels={'protein': 'Grams', 'index': 'Date'})
            st.plotly_chart(fig_protein, use_container_width=True)

        # Recent entries
        st.subheader("📅 Recent Entries")
        display_df = df.copy()
        display_df.index = display_df.index.strftime('%Y-%m-%d')
        st.dataframe(display_df[['sleep', 'exercise', 'pt_quota', 'water', 'protein']].tail(10),
                    use_container_width=True)

    else:
        st.info("No data logged yet. Go to 'Log Today' to start tracking!")

# Tab 3: Leaderboard
with tab3:
    st.header("🏆 Leaderboard")

    if st.session_state.data:
        # Calculate scores for each user
        leaderboard_data = []

        for user, user_logs in st.session_state.data.items():
            if not user_logs:
                continue

            df = pd.DataFrame.from_dict(user_logs, orient='index')

            # Calculate various metrics
            total_days = len(df)
            sleep_score = (df['sleep'] >= 8).sum()
            exercise_score = df['exercise'].sum()
            pt_score = df['pt_quota'].sum()
            avg_water = df['water'].mean()
            avg_protein = df['protein'].mean()

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
                'Sleep Goals Met': sleep_score,
                'Exercise Days': exercise_score,
                'PT Days': pt_score,
                'Avg Water (oz)': f"{avg_water:.0f}",
                'Avg Protein (g)': f"{avg_protein:.0f}",
                'Overall Score': overall_score
            })

        # Create leaderboard DataFrame
        lb_df = pd.DataFrame(leaderboard_data)
        lb_df = lb_df.sort_values('Overall Score', ascending=False).reset_index(drop=True)
        lb_df.index = lb_df.index + 1  # Start ranking from 1

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

    if st.session_state.data:
        all_data = []

        for user, user_logs in st.session_state.data.items():
            for date_str, metrics in user_logs.items():
                all_data.append({
                    'User': user,
                    'Date': pd.to_datetime(date_str),
                    **metrics
                })

        if all_data:
            df_all = pd.DataFrame(all_data)

            # Group comparison
            st.subheader("👥 Group Comparison")

            metric_choice = st.selectbox(
                "Select metric to compare:",
                ['sleep', 'water', 'protein']
            )

            fig = px.box(df_all, x='User', y=metric_choice,
                        title=f'{metric_choice.capitalize()} Distribution by User',
                        color='User')
            st.plotly_chart(fig, use_container_width=True)

            # Timeline comparison
            st.subheader("📅 Timeline Comparison")

            df_avg = df_all.groupby(['Date', 'User'])[metric_choice].mean().reset_index()

            fig_timeline = px.line(df_avg, x='Date', y=metric_choice,
                                  color='User', title=f'{metric_choice.capitalize()} Over Time')
            st.plotly_chart(fig_timeline, use_container_width=True)

            # Success rates
            st.subheader("✅ Success Rates")

            col1, col2 = st.columns(2)

            with col1:
                exercise_rates = df_all.groupby('User')['exercise'].mean() * 100
                fig_ex = px.bar(exercise_rates, title='Exercise Completion Rate',
                               labels={'value': 'Percentage', 'User': 'User'})
                st.plotly_chart(fig_ex, use_container_width=True)

            with col2:
                pt_rates = df_all.groupby('User')['pt_quota'].mean() * 100
                fig_pt = px.bar(pt_rates, title='PT Quota Completion Rate',
                               labels={'value': 'Percentage', 'User': 'User'})
                st.plotly_chart(fig_pt, use_container_width=True)

    else:
        st.info("No data available yet for analytics!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for tracking daily progress | 🏆 Keep grinding!")

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta

# Page config
st.set_page_config(
    page_title="Bahaha Dilly Dailies",
    page_icon="🏆",
    layout="wide"
)

# User configurations with their custom KPIs
USER_CONFIG = {
    "bobby": {
        "columns": ['user', 'date', 'strength_workout', 'pt_mobility', 'eating_enough', 'rhr', 'vo2max', 'notes', 'timestamp'],
        "weekly_goals": {'strength_workout': 3},
        "daily_goals": {'pt_mobility': True, 'eating_enough': True}
    },
    "hansa": {
        "columns": ['user', 'date', 'strength_workout', 'mobility', 'glute_exercises', 'cardio', 'added_sugar', 'notes', 'timestamp'],
        "weekly_goals": {'strength_workout': 2, 'glute_exercises': 2, 'cardio': 4},
        "daily_goals": {'mobility': True, 'added_sugar': 25}  # less than 25g
    },
    "anne": {
        "columns": ['user', 'date', 'sleep_rested', 'knee_pt_minutes', 'back_pt_minutes', 'protein', 'water',
                   'cardio_minutes', 'strength_minutes', 'mental_health_days', 'notes', 'timestamp'],
        "weekly_goals": {'cardio_minutes': 4, 'strength_minutes': 2},  # 4x and 2x per week
        "daily_goals": {'sleep_rested': True, 'knee_pt_minutes': True, 'back_pt_minutes': True,
                       'protein': 100, 'water': 80}
    },
    "vinay": {
        "columns": ['user', 'date', 'sleep_hours', 'drinks_daily', 'pt_minutes', 'red_meat',
                   'strength_workout', 'workout_minutes', 'notes', 'timestamp'],
        "weekly_goals": {'strength_workout': 2, 'drinks_daily': 12, 'red_meat': 7},  # max per week
        "daily_goals": {'drinks_daily': 2, 'pt_minutes': True, 'workout_minutes': True}
    },
    "harini": {
        "columns": ['user', 'date', 'screen_time_minutes', 'yoga', 'strength_workout',
                   'outdoor_walking_minutes', 'notes', 'timestamp'],
        "weekly_goals": {'yoga': 2, 'strength_workout': 2},
        "daily_goals": {'outdoor_walking_minutes': True}
    }
}

# Connect to Google Sheets
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def load_user_data(user):
    """Load data from user's specific Google Sheet tab"""
    try:
        conn = get_connection()
        df = conn.read(worksheet=user, ttl="0")  # Read from user's sheet tab

        # If sheet is empty, return empty DataFrame with correct columns
        if df.empty or len(df.columns) == 0:
            return pd.DataFrame(columns=USER_CONFIG[user]['columns'])

        return df
    except Exception as e:
        st.error(f"Error loading data for {user}: {e}")
        return pd.DataFrame(columns=USER_CONFIG[user]['columns'])

def save_user_data(user, df):
    """Save data to user's specific Google Sheet tab"""
    try:
        conn = get_connection()
        conn.update(worksheet=user, data=df)
        return True
    except Exception as e:
        st.error(f"Error saving data for {user}: {e}")
        return False

# App title
st.title("🏆 Bahaha Dilly Dailies")
st.markdown("### Track your daily KPIs and compete with friends!")

# Sidebar for user selection
st.sidebar.title("User Login")
users = ["anne", "bobby", "hansa", "vinay", "harini"]
selected_user = st.sidebar.selectbox("Select your name:", users)

# Load user-specific data
if 'current_user' not in st.session_state or st.session_state.current_user != selected_user:
    st.session_state.current_user = selected_user
    st.session_state.df = load_user_data(selected_user)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {selected_user.capitalize()}'s Goals")

# Display user-specific goals in sidebar
if selected_user == "bobby":
    st.sidebar.markdown("""
    - 💪 Strength: 3x/week
    - 🧘 PT/Mobility: Daily
    - 🍽️ Eating Enough: Daily
    - ❤️ Track RHR & VO2max
    """)
elif selected_user == "hansa":
    st.sidebar.markdown("""
    - 💪 Strength: 2x/week
    - 🧘 Mobility: Daily
    - 🍑 Glute Exercises: 2x/week
    - 🏃 Cardio: 4x/week
    - 🍬 Added Sugar: <25g daily
    """)
elif selected_user == "anne":
    st.sidebar.markdown("""
    - 💤 Sleep: Feel rested?
    - 🦵 Knee PT: Daily (minutes)
    - 🧘 Back PT: Daily (minutes)
    - 🥩 Protein: 100g daily
    - 💧 Water: 80oz daily
    - 🏃 Cardio: 4x/week
    - 💪 Strength: 2x/week
    - 🧠 Mental Health: Track days
    """)
elif selected_user == "vinay":
    st.sidebar.markdown("""
    - 💤 Sleep: Track hours
    - 🍺 Drinks: 2 daily, 12/week max
    - 🧘 PT: Daily minutes
    - 🥩 Red Meat: Track daily/weekly
    - 💪 Strength: 2x/week
    - 🏃 Workout: Daily minutes
    """)
elif selected_user == "harini":
    st.sidebar.markdown("""
    - 📱 Screen Time: Daily minutes
    - 🧘 Yoga: 2x/week
    - 💪 Strength: 2x/week
    - 🌳 Outdoor Walking: Daily minutes
    """)

# Main tabs
tab1, tab2, tab3 = st.tabs(["📝 Log Today", "📊 My Progress", "🏆 Leaderboard"])

# Tab 1: Log Today's KPIs (Custom per user)
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

        new_entry = {'user': selected_user, 'date': today}

        # Bobby's custom form
        if selected_user == "bobby":
            col1, col2 = st.columns(2)

            with col1:
                new_entry['strength_workout'] = st.checkbox(
                    "💪 Strength Workout Today",
                    value=bool(existing_data.get('strength_workout', False)),
                    help="Goal: 3x per week"
                )

                new_entry['pt_mobility'] = st.checkbox(
                    "🧘 PT/Mobility Done",
                    value=bool(existing_data.get('pt_mobility', False)),
                    help="Daily goal"
                )

                new_entry['eating_enough'] = st.checkbox(
                    "🍽️ Eating Enough Today",
                    value=bool(existing_data.get('eating_enough', False)),
                    help="Daily goal"
                )

            with col2:
                new_entry['rhr'] = st.number_input(
                    "❤️ Resting Heart Rate (bpm)",
                    min_value=0,
                    max_value=200,
                    value=int(existing_data.get('rhr', 0)),
                    help="Optional tracking"
                )

                new_entry['vo2max'] = st.number_input(
                    "🫁 VO2 Max",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(existing_data.get('vo2max', 0.0)),
                    step=0.1,
                    help="Optional tracking"
                )

        # Hansa's custom form
        elif selected_user == "hansa":
            col1, col2 = st.columns(2)

            with col1:
                new_entry['strength_workout'] = st.checkbox(
                    "💪 Strength Workout Today",
                    value=bool(existing_data.get('strength_workout', False)),
                    help="Goal: 2x per week"
                )

                new_entry['mobility'] = st.checkbox(
                    "🧘 Mobility Done",
                    value=bool(existing_data.get('mobility', False)),
                    help="Daily goal"
                )

                new_entry['glute_exercises'] = st.checkbox(
                    "🍑 Glute Exercises Done",
                    value=bool(existing_data.get('glute_exercises', False)),
                    help="Goal: 2x per week"
                )

            with col2:
                new_entry['cardio'] = st.checkbox(
                    "🏃 Cardio Done",
                    value=bool(existing_data.get('cardio', False)),
                    help="Goal: 4x per week"
                )

                new_entry['added_sugar'] = st.number_input(
                    "🍬 Added Sugar (grams)",
                    min_value=0,
                    max_value=200,
                    value=int(existing_data.get('added_sugar', 0)),
                    help="Goal: Less than 25g daily"
                )

        # Anne's custom form
        elif selected_user == "anne":
            col1, col2 = st.columns(2)

            with col1:
                new_entry['sleep_rested'] = st.checkbox(
                    "💤 Woke Up Feeling Rested",
                    value=bool(existing_data.get('sleep_rested', False))
                )

                new_entry['knee_pt_minutes'] = st.number_input(
                    "🦵 Knee PT (minutes)",
                    min_value=0,
                    max_value=300,
                    value=int(existing_data.get('knee_pt_minutes', 0)),
                    help="Daily goal"
                )

                new_entry['back_pt_minutes'] = st.number_input(
                    "🧘 Back PT (minutes)",
                    min_value=0,
                    max_value=300,
                    value=int(existing_data.get('back_pt_minutes', 0)),
                    help="Daily goal"
                )

                new_entry['protein'] = st.number_input(
                    "🥩 Protein (grams)",
                    min_value=0,
                    max_value=500,
                    value=int(existing_data.get('protein', 0)),
                    help="Goal: 100g daily"
                )

                new_entry['water'] = st.number_input(
                    "💧 Water (oz)",
                    min_value=0,
                    max_value=300,
                    value=int(existing_data.get('water', 0)),
                    help="Goal: 80oz daily"
                )

            with col2:
                new_entry['cardio_minutes'] = st.number_input(
                    "🏃 Cardio (minutes)",
                    min_value=0,
                    max_value=500,
                    value=int(existing_data.get('cardio_minutes', 0)),
                    help="Goal: 4x per week"
                )

                new_entry['strength_minutes'] = st.number_input(
                    "💪 Strength Training (minutes)",
                    min_value=0,
                    max_value=500,
                    value=int(existing_data.get('strength_minutes', 0)),
                    help="Goal: 2x per week"
                )

                new_entry['mental_health_days'] = st.number_input(
                    "🧠 Days Since Last Bad Mental Health Day",
                    min_value=0,
                    max_value=1000,
                    value=int(existing_data.get('mental_health_days', 0)),
                    help="Track your mental health streak"
                )

        # Vinay's custom form
        elif selected_user == "vinay":
            col1, col2 = st.columns(2)

            with col1:
                new_entry['sleep_hours'] = st.number_input(
                    "💤 Sleep (hours)",
                    min_value=0.0,
                    max_value=24.0,
                    value=float(existing_data.get('sleep_hours', 0.0)),
                    step=0.5
                )

                new_entry['drinks_daily'] = st.number_input(
                    "🍺 Drinks Today",
                    min_value=0,
                    max_value=20,
                    value=int(existing_data.get('drinks_daily', 0)),
                    help="Goal: 2 daily max, 12 weekly max"
                )

                new_entry['pt_minutes'] = st.number_input(
                    "🧘 PT (minutes)",
                    min_value=0,
                    max_value=300,
                    value=int(existing_data.get('pt_minutes', 0)),
                    help="Daily goal"
                )

            with col2:
                new_entry['red_meat'] = st.checkbox(
                    "🥩 Red Meat Today",
                    value=bool(existing_data.get('red_meat', False)),
                    help="Track daily and weekly consumption"
                )

                new_entry['strength_workout'] = st.checkbox(
                    "💪 Strength Workout Today",
                    value=bool(existing_data.get('strength_workout', False)),
                    help="Goal: 2x per week"
                )

                new_entry['workout_minutes'] = st.number_input(
                    "🏃 Total Workout (minutes)",
                    min_value=0,
                    max_value=500,
                    value=int(existing_data.get('workout_minutes', 0)),
                    help="Daily workout minutes"
                )

        # Harini's custom form
        elif selected_user == "harini":
            col1, col2 = st.columns(2)

            with col1:
                new_entry['screen_time_minutes'] = st.number_input(
                    "📱 Screen Time (minutes)",
                    min_value=0,
                    max_value=1440,
                    value=int(existing_data.get('screen_time_minutes', 0)),
                    help="Track daily screen time"
                )

                new_entry['yoga'] = st.checkbox(
                    "🧘 Yoga Done",
                    value=bool(existing_data.get('yoga', False)),
                    help="Goal: 2x per week"
                )

            with col2:
                new_entry['strength_workout'] = st.checkbox(
                    "💪 Strength Workout Done",
                    value=bool(existing_data.get('strength_workout', False)),
                    help="Goal: 2x per week"
                )

                new_entry['outdoor_walking_minutes'] = st.number_input(
                    "🌳 Outdoor Walking (minutes)",
                    min_value=0,
                    max_value=500,
                    value=int(existing_data.get('outdoor_walking_minutes', 0)),
                    help="Daily outdoor walking"
                )

        # Common notes field for all users
        new_entry['notes'] = st.text_area(
            "📝 Notes (optional)",
            value=existing_data.get('notes', ''),
            placeholder="Any additional notes about your day..."
        )

        new_entry['timestamp'] = datetime.now().isoformat()

        submitted = st.form_submit_button("💾 Save Today's Data", use_container_width=True)

        if submitted:
            # Create new row
            new_row = pd.DataFrame([new_entry])

            # Remove old entry if updating
            if already_logged:
                st.session_state.df = st.session_state.df[
                    ~((st.session_state.df['user'] == selected_user) &
                      (st.session_state.df['date'] == today))
                ]

            # Add new row
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

            # Save to Google Sheets
            if save_user_data(selected_user, st.session_state.df):
                st.success("✅ Data saved successfully!")
                st.balloons()
            else:
                st.error("Failed to save to Google Sheets")

# Tab 2: My Progress (Custom per user)
with tab2:
    st.header(f"{selected_user.capitalize()}'s Progress")

    user_df = st.session_state.df.copy()

    if not user_df.empty and len(user_df) > 0:
        user_df['date'] = pd.to_datetime(user_df['date'])
        user_df = user_df.sort_values('date')

        # Summary metrics - customize per user
        st.subheader("📊 Summary Statistics")

        if selected_user == "bobby":
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                strength_pct = (user_df['strength_workout'].sum() / len(user_df)) * 100 if len(user_df) > 0 else 0
                st.metric("Strength Rate", f"{strength_pct:.0f}%", help="Goal: 43% (3/7 days)")

            with col2:
                pt_pct = (user_df['pt_mobility'].sum() / len(user_df)) * 100 if len(user_df) > 0 else 0
                st.metric("PT/Mobility Rate", f"{pt_pct:.0f}%", help="Goal: 100%")

            with col3:
                eating_pct = (user_df['eating_enough'].sum() / len(user_df)) * 100 if len(user_df) > 0 else 0
                st.metric("Eating Enough Rate", f"{eating_pct:.0f}%", help="Goal: 100%")

            with col4:
                avg_rhr = user_df[user_df['rhr'] > 0]['rhr'].mean() if (user_df['rhr'] > 0).any() else 0
                st.metric("Avg RHR", f"{avg_rhr:.0f} bpm")

        elif selected_user == "hansa":
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                strength_pct = (user_df['strength_workout'].sum() / len(user_df)) * 100
                st.metric("Strength Rate", f"{strength_pct:.0f}%", help="Goal: 29% (2/7 days)")

            with col2:
                mobility_pct = (user_df['mobility'].sum() / len(user_df)) * 100
                st.metric("Mobility Rate", f"{mobility_pct:.0f}%", help="Goal: 100%")

            with col3:
                glute_pct = (user_df['glute_exercises'].sum() / len(user_df)) * 100
                st.metric("Glute Ex Rate", f"{glute_pct:.0f}%", help="Goal: 29% (2/7 days)")

            with col4:
                cardio_pct = (user_df['cardio'].sum() / len(user_df)) * 100
                st.metric("Cardio Rate", f"{cardio_pct:.0f}%", help="Goal: 57% (4/7 days)")

            with col5:
                avg_sugar = user_df['added_sugar'].mean()
                st.metric("Avg Sugar", f"{avg_sugar:.0f}g", help="Goal: <25g")

        elif selected_user == "anne":
            col1, col2, col3 = st.columns(3)

            with col1:
                sleep_pct = (user_df['sleep_rested'].sum() / len(user_df)) * 100
                st.metric("Rested Sleep %", f"{sleep_pct:.0f}%")

                avg_knee_pt = user_df['knee_pt_minutes'].mean()
                st.metric("Avg Knee PT", f"{avg_knee_pt:.0f} min")

                avg_back_pt = user_df['back_pt_minutes'].mean()
                st.metric("Avg Back PT", f"{avg_back_pt:.0f} min")

            with col2:
                avg_protein = user_df['protein'].mean()
                st.metric("Avg Protein", f"{avg_protein:.0f}g", help="Goal: 100g")

                avg_water = user_df['water'].mean()
                st.metric("Avg Water", f"{avg_water:.0f}oz", help="Goal: 80oz")

            with col3:
                cardio_days = (user_df['cardio_minutes'] > 0).sum()
                st.metric("Cardio Days", f"{cardio_days}", help="Goal: 4x/week")

                strength_days = (user_df['strength_minutes'] > 0).sum()
                st.metric("Strength Days", f"{strength_days}", help="Goal: 2x/week")

                current_mh = user_df['mental_health_days'].iloc[-1] if len(user_df) > 0 else 0
                st.metric("Mental Health Streak", f"{current_mh} days")

        elif selected_user == "vinay":
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                avg_sleep = user_df['sleep_hours'].mean()
                st.metric("Avg Sleep", f"{avg_sleep:.1f}h")

            with col2:
                avg_drinks = user_df['drinks_daily'].mean()
                st.metric("Avg Drinks/Day", f"{avg_drinks:.1f}", help="Goal: ≤2")

            with col3:
                avg_pt = user_df['pt_minutes'].mean()
                st.metric("Avg PT", f"{avg_pt:.0f} min")

            with col4:
                strength_pct = (user_df['strength_workout'].sum() / len(user_df)) * 100
                st.metric("Strength Rate", f"{strength_pct:.0f}%", help="Goal: 29% (2/7 days)")

        elif selected_user == "harini":
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                avg_screen = user_df['screen_time_minutes'].mean()
                st.metric("Avg Screen Time", f"{avg_screen:.0f} min")

            with col2:
                yoga_pct = (user_df['yoga'].sum() / len(user_df)) * 100
                st.metric("Yoga Rate", f"{yoga_pct:.0f}%", help="Goal: 29% (2/7 days)")

            with col3:
                strength_pct = (user_df['strength_workout'].sum() / len(user_df)) * 100
                st.metric("Strength Rate", f"{strength_pct:.0f}%", help="Goal: 29% (2/7 days)")

            with col4:
                avg_walking = user_df['outdoor_walking_minutes'].mean()
                st.metric("Avg Walking", f"{avg_walking:.0f} min")

        # Charts section
        st.subheader("📈 Trends")

        # Create custom charts based on user
        if selected_user == "bobby":
            col1, col2 = st.columns(2)
            with col1:
                # Strength workout trend
                user_df['strength_cumsum'] = user_df['strength_workout'].cumsum()
                fig = px.line(user_df, x='date', y='strength_cumsum',
                            title='Cumulative Strength Workouts')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # RHR trend if data exists
                if (user_df['rhr'] > 0).any():
                    fig = px.line(user_df[user_df['rhr'] > 0], x='date', y='rhr',
                                title='Resting Heart Rate')
                    st.plotly_chart(fig, use_container_width=True)

        elif selected_user == "anne":
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(user_df, x='date', y='protein', title='Daily Protein',
                           labels={'protein': 'Grams'})
                fig.add_hline(y=100, line_dash="dash", line_color="green",
                            annotation_text="Goal: 100g")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(user_df, x='date', y='water', title='Daily Water',
                           labels={'water': 'Ounces'})
                fig.add_hline(y=80, line_dash="dash", line_color="blue",
                            annotation_text="Goal: 80oz")
                st.plotly_chart(fig, use_container_width=True)

            # PT minutes
            fig = go.Figure()
            fig.add_trace(go.Bar(x=user_df['date'], y=user_df['knee_pt_minutes'],
                                name='Knee PT', marker_color='lightblue'))
            fig.add_trace(go.Bar(x=user_df['date'], y=user_df['back_pt_minutes'],
                                name='Back PT', marker_color='lightcoral'))
            fig.update_layout(title='PT Minutes', barmode='stack')
            st.plotly_chart(fig, use_container_width=True)

        elif selected_user == "hansa":
            fig = px.bar(user_df, x='date', y='added_sugar', title='Daily Added Sugar',
                       labels={'added_sugar': 'Grams'})
            fig.add_hline(y=25, line_dash="dash", line_color="red",
                        annotation_text="Goal: <25g")
            st.plotly_chart(fig, use_container_width=True)

        elif selected_user == "vinay":
            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(user_df, x='date', y='sleep_hours', title='Sleep Hours')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(user_df, x='date', y='drinks_daily', title='Daily Drinks')
                fig.add_hline(y=2, line_dash="dash", line_color="red",
                            annotation_text="Daily Goal: 2")
                st.plotly_chart(fig, use_container_width=True)

        elif selected_user == "harini":
            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(user_df, x='date', y='screen_time_minutes',
                            title='Screen Time')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(user_df, x='date', y='outdoor_walking_minutes',
                           title='Outdoor Walking Minutes')
                st.plotly_chart(fig, use_container_width=True)

        # Recent entries
        st.subheader("📅 Recent Entries")
        display_cols = [col for col in user_df.columns if col not in ['user', 'timestamp', 'notes']]
        display_df = user_df[display_cols].tail(10).copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_df, use_container_width=True)

    else:
        st.info("No data logged yet. Go to 'Log Today' to start tracking!")

# Tab 3: Leaderboard
with tab3:
    st.header("🏆 Leaderboard")

    st.info("💡 The leaderboard calculates scores based on each person's individual goals and completion rates.")

    leaderboard_data = []

    for user in users:
        user_specific_df = load_user_data(user)

        if user_specific_df.empty or len(user_specific_df) == 0:
            continue

        user_specific_df['date'] = pd.to_datetime(user_specific_df['date'])
        total_days = len(user_specific_df)

        # Calculate score based on user-specific goals
        score = 0

        if user == "bobby":
            # Weekly goals: strength 3x
            # Daily goals: PT/mobility, eating enough
            strength_rate = user_specific_df['strength_workout'].sum() / total_days if total_days > 0 else 0
            pt_rate = user_specific_df['pt_mobility'].sum() / total_days if total_days > 0 else 0
            eating_rate = user_specific_df['eating_enough'].sum() / total_days if total_days > 0 else 0

            score = (strength_rate * 30) + (pt_rate * 35) + (eating_rate * 35)

        elif user == "hansa":
            # Weekly goals: strength 2x, glute 2x, cardio 4x
            # Daily goals: mobility, sugar <25g
            strength_rate = user_specific_df['strength_workout'].sum() / total_days if total_days > 0 else 0
            mobility_rate = user_specific_df['mobility'].sum() / total_days if total_days > 0 else 0
            glute_rate = user_specific_df['glute_exercises'].sum() / total_days if total_days > 0 else 0
            cardio_rate = user_specific_df['cardio'].sum() / total_days if total_days > 0 else 0
            sugar_rate = (user_specific_df['added_sugar'] <= 25).sum() / total_days if total_days > 0 else 0

            score = (strength_rate * 15) + (mobility_rate * 25) + (glute_rate * 15) + (cardio_rate * 20) + (sugar_rate * 25)

        elif user == "anne":
            # Daily goals: sleep rested, knee PT, back PT, protein 100g, water 80oz
            # Weekly goals: cardio 4x, strength 2x
            sleep_rate = user_specific_df['sleep_rested'].sum() / total_days if total_days > 0 else 0
            knee_pt_rate = (user_specific_df['knee_pt_minutes'] > 0).sum() / total_days if total_days > 0 else 0
            back_pt_rate = (user_specific_df['back_pt_minutes'] > 0).sum() / total_days if total_days > 0 else 0
            protein_rate = (user_specific_df['protein'] >= 100).sum() / total_days if total_days > 0 else 0
            water_rate = (user_specific_df['water'] >= 80).sum() / total_days if total_days > 0 else 0
            cardio_rate = (user_specific_df['cardio_minutes'] > 0).sum() / total_days if total_days > 0 else 0
            strength_rate = (user_specific_df['strength_minutes'] > 0).sum() / total_days if total_days > 0 else 0

            score = (sleep_rate * 15) + (knee_pt_rate * 15) + (back_pt_rate * 15) + \
                   (protein_rate * 15) + (water_rate * 15) + (cardio_rate * 12.5) + (strength_rate * 12.5)

        elif user == "vinay":
            # Daily goals: drinks ≤2, PT minutes, workout minutes
            # Weekly goals: strength 2x, drinks ≤12/week
            drinks_rate = (user_specific_df['drinks_daily'] <= 2).sum() / total_days if total_days > 0 else 0
            pt_rate = (user_specific_df['pt_minutes'] > 0).sum() / total_days if total_days > 0 else 0
            workout_rate = (user_specific_df['workout_minutes'] > 0).sum() / total_days if total_days > 0 else 0
            strength_rate = user_specific_df['strength_workout'].sum() / total_days if total_days > 0 else 0

            score = (drinks_rate * 25) + (pt_rate * 25) + (workout_rate * 25) + (strength_rate * 25)

        elif user == "harini":
            # Weekly goals: yoga 2x, strength 2x
            # Daily goals: outdoor walking
            yoga_rate = user_specific_df['yoga'].sum() / total_days if total_days > 0 else 0
            strength_rate = user_specific_df['strength_workout'].sum() / total_days if total_days > 0 else 0
            walking_rate = (user_specific_df['outdoor_walking_minutes'] > 0).sum() / total_days if total_days > 0 else 0

            score = (yoga_rate * 30) + (strength_rate * 30) + (walking_rate * 40)

        leaderboard_data.append({
            'User': user.capitalize(),
            'Total Days': total_days,
            'Overall Score': round(score, 1)
        })

    if leaderboard_data:
        # Create leaderboard DataFrame
        lb_df = pd.DataFrame(leaderboard_data)
        lb_df = lb_df.sort_values('Overall Score', ascending=False).reset_index(drop=True)
        lb_df.index = lb_df.index + 1

        # Display podium
        st.subheader("🏅 Rankings")
        cols = st.columns(len(lb_df))
        medals = ['🥇', '🥈', '🥉', '🏅', '🏅']

        for idx, (i, row) in enumerate(lb_df.iterrows()):
            with cols[idx]:
                medal = medals[idx] if idx < len(medals) else '🏅'
                st.markdown(f"### {medal} #{i}")
                st.markdown(f"### {row['User']}")
                st.metric("Score", f"{row['Overall Score']:.1f}/100")
                st.caption(f"{row['Total Days']} days logged")

        # Detailed leaderboard
        st.subheader("📊 Detailed Rankings")
        st.dataframe(lb_df, use_container_width=True)

        st.caption("""
        **Scoring System**: Each person is scored out of 100 based on their individual goals.
        Scores reflect what percentage of personal goals were met across all logged days.
        """)

    else:
        st.info("No data available yet. Start logging to see the leaderboard!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for tracking daily progress | 🏆 Keep grinding! Happy New Year!!")

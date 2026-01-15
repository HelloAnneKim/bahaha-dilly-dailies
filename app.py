import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import pytz

# Page config
st.set_page_config(
    page_title="Bahaha Dilly Dailies",
    page_icon="🏆",
    layout="wide"
)

# Configuration rows in each user's sheet:
# Row 1: Column names
# Row 2: display_name
# Row 3: emoji
# Row 4: units
# Row 5: type (boolean, int, float, note, date, timestamp)
# Row 6: has_goal (TRUE/FALSE)
# Row 7: weekly_or_daily_goal (daily/weekly_total/count_per_week/empty)
# Row 8: goal_target (number or TRUE/FALSE)
# Row 9: goal_direction (at_least/at_most/empty)
# Row 10: help_text
# Row 11+: Data rows

# Helper function to get current tracking date (deadline is 3am ET)
def get_tracking_date():
    """
    Returns the current tracking date.
    If it's before 3am ET, returns yesterday's date.
    If it's 3am ET or later, returns today's date.
    """
    et_tz = pytz.timezone('US/Eastern')
    current_time_et = datetime.now(et_tz)

    # If it's before 3am ET, use yesterday's date
    if current_time_et.hour < 3:
        tracking_date = (current_time_et - timedelta(days=1)).date()
    else:
        tracking_date = current_time_et.date()

    return tracking_date

def get_tracking_date_str():
    return str(get_tracking_date())

# Helper function to get yesterday's date
def get_yesterday():
    """Returns the day before the tracking date"""
    yesterday = get_tracking_date() - timedelta(days=1)
    return yesterday

# Connect to Google Sheets
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def load_users():
    """Load list of users from the 'users' tab, column A, starting at row 2"""
    try:
        conn = get_connection()
        df = conn.read(worksheet="users", ttl="60")  # Cache for 60 seconds
        
        if df.empty or len(df.columns) == 0:
            return []
        
        # Get column A (first column), skip row 0 (header), get all non-empty values
        users = df.iloc[:, 0].dropna().tolist()
        # Remove header if it exists and convert to lowercase
        users = [str(u).lower().strip() for u in users if str(u).lower().strip() and str(u).lower().strip() != 'user']
        return users
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return []

def load_column_config(user, df=None):
    """Load column configuration from user's sheet (rows 1-10)
    If df is provided, use it instead of making a new API call"""
    try:
        if df is None:
            conn = get_connection()
            # Read first 10 rows to get config
            # st-gsheets-connection uses row 1 as headers by default
            config_df = conn.read(worksheet=user, ttl="60", usecols=None, nrows=10)  # Cache for 60 seconds
        else:
            # Use provided df, but we need first 10 rows (which are rows 2-11 in the sheet)
            # Since row 1 is used as headers, iloc[0:9] gives us rows 2-10
            if len(df) < 9:
                return None
            config_df = df.iloc[0:9].copy()  # Get first 9 data rows (rows 2-10 of sheet)
            config_df.columns = df.columns  # Preserve column names
        
        if config_df.empty or len(config_df) < 9:  # Need at least 9 rows after header
            return None
        
        # Column names are in config_df.columns (from row 1 of the sheet)
        column_names = [str(col) for col in config_df.columns]
        num_cols = len(column_names)
        
        # Build config dictionary
        # Since row 1 is used as headers:
        #   config_df.iloc[0] = row 2 (display_name)
        #   config_df.iloc[1] = row 3 (emoji)
        #   config_df.iloc[2] = row 4 (units)
        #   etc.
        config = {}
        
        for col_idx, col_name in enumerate(column_names):
            if pd.isna(col_name) or str(col_name).strip() == '' or str(col_name).strip().lower() in ['nan', 'none']:
                continue
                
            col_name = str(col_name).strip()
            
            if col_idx >= num_cols:
                continue
            
            try:
                # Access by numeric column index
                config[col_name] = {
                    'display_name': str(config_df.iloc[0, col_idx]) if col_idx < num_cols and 0 < len(config_df) and not pd.isna(config_df.iloc[0, col_idx]) else col_name,
                    'emoji': str(config_df.iloc[1, col_idx]) if col_idx < num_cols and 1 < len(config_df) and not pd.isna(config_df.iloc[1, col_idx]) else '',
                    'units': str(config_df.iloc[2, col_idx]) if col_idx < num_cols and 2 < len(config_df) and not pd.isna(config_df.iloc[2, col_idx]) else '',
                    'type': str(config_df.iloc[3, col_idx]).lower() if col_idx < num_cols and 3 < len(config_df) and not pd.isna(config_df.iloc[3, col_idx]) else 'note',
                    'has_goal': str(config_df.iloc[4, col_idx]).upper() == 'TRUE' if col_idx < num_cols and 4 < len(config_df) and not pd.isna(config_df.iloc[4, col_idx]) else False,
                    'weekly_or_daily_goal': str(config_df.iloc[5, col_idx]).lower() if col_idx < num_cols and 5 < len(config_df) and not pd.isna(config_df.iloc[5, col_idx]) else '',
                    'goal_target': config_df.iloc[6, col_idx] if col_idx < num_cols and 6 < len(config_df) and not pd.isna(config_df.iloc[6, col_idx]) else None,
                    'goal_direction': str(config_df.iloc[7, col_idx]).lower() if col_idx < num_cols and 7 < len(config_df) and not pd.isna(config_df.iloc[7, col_idx]) else '',
                    'help_text': str(config_df.iloc[8, col_idx]) if col_idx < num_cols and 8 < len(config_df) and not pd.isna(config_df.iloc[8, col_idx]) else ''
                }
            except (IndexError, KeyError) as e:
                # Skip this column if we can't access it
                continue
        
        return config
    except Exception as e:
        error_msg = str(e) if e else "Unknown error"
        error_type = type(e).__name__
        st.error(f"Error loading column config for {user}: {error_type} - {error_msg}")
        st.exception(e)
        return None

@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_all_users_data(users_list):
    """Load data for all users at once and cache the result"""
    all_data = {}
    conn = get_connection()
    
    for user in users_list:
        try:
            df = conn.read(worksheet=user, ttl="0")  # Use 0 here since we're caching at this level
            
            if df.empty or len(df.columns) == 0:
                all_data[user] = (pd.DataFrame(), None)
                continue
            
            # Get column config from the same dataframe to avoid duplicate API call
            config = load_column_config(user, df)
            if config is None:
                all_data[user] = (pd.DataFrame(), None)
                continue
            
            # Skip first 10 rows (config rows), use row 0 for column names
            CONFIG_ROWS_COUNT = 10
            if len(df) <= CONFIG_ROWS_COUNT:
                # No data rows yet
                all_data[user] = (pd.DataFrame(columns=list(config.keys())), config)
                continue
            
            # Get data starting from row 10 (index 10)
            data_df = df.iloc[10:].copy()
            data_df.columns = df.columns  # Preserve column names from row 0
            
            # Reset index
            data_df = data_df.reset_index(drop=True)
            
            all_data[user] = (data_df, config)
        except Exception as e:
            error_msg = str(e) if e else "Unknown error"
            error_type = type(e).__name__
            st.error(f"Error loading data for user '{user}': {error_type} - {error_msg}")
            st.exception(e)
            raise
    return all_data

def load_user_data(user):
    """Load data from user's specific Google Sheet tab, skipping config rows (1-10)"""
    try:
        conn = get_connection()
        df = conn.read(worksheet=user, ttl="60")  # Cache for 60 seconds

        if df.empty or len(df.columns) == 0:
            return pd.DataFrame(), None
        
        # Get column config from the same dataframe to avoid duplicate API call
        config = load_column_config(user, df)
        if config is None:
            return pd.DataFrame(), None
        
        # Skip first 10 rows (config rows), use row 0 for column names
        CONFIG_ROWS_COUNT = 10
        if len(df) <= CONFIG_ROWS_COUNT:
            # No data rows yet
            return pd.DataFrame(columns=list(config.keys())), config
        
        # Get data starting from row 10 (index 10)
        data_df = df.iloc[10:].copy()
        data_df.columns = df.columns  # Preserve column names from row 0
        
        # Reset index
        data_df = data_df.reset_index(drop=True)
        
        return data_df, config
    except Exception as e:
        error_msg = str(e) if e else "Unknown error"
        error_type = type(e).__name__
        st.error(f"Error loading data for {user}: {error_type} - {error_msg}")
        st.exception(e)
        return pd.DataFrame(), None

def save_user_data(user, data_df, config):
    """Save data to user's specific Google Sheet tab, preserving config rows (1-10)"""
    try:
        conn = get_connection()
        
        # Build config rows DataFrame from config parameter (no need to read again)
        if config:
            column_names = list(config.keys())
            
            # Create config rows
            config_rows = []
            config_rows.append(column_names)  # Row 1: column names
            config_rows.append([config[col]['display_name'] for col in column_names])  # Row 2
            config_rows.append([config[col]['emoji'] for col in column_names])  # Row 3
            config_rows.append([config[col]['units'] for col in column_names])  # Row 4
            config_rows.append([config[col]['type'] for col in column_names])  # Row 5
            config_rows.append([str(config[col]['has_goal']).upper() for col in column_names])  # Row 6
            config_rows.append([config[col]['weekly_or_daily_goal'] for col in column_names])  # Row 7
            config_rows.append([config[col]['goal_target'] if config[col]['goal_target'] is not None else '' for col in column_names])  # Row 8
            config_rows.append([config[col]['goal_direction'] for col in column_names])  # Row 9
            config_rows.append([config[col]['help_text'] for col in column_names])  # Row 10
            
            config_df = pd.DataFrame(config_rows, columns=column_names)
            
            # Combine config rows with data rows
            # Ensure data_df has all columns from config
            for col in column_names:
                if col not in data_df.columns:
                    data_df[col] = ''
            
            # Reorder columns to match config
            data_df = data_df[column_names]
            
            # Convert boolean columns to 0/1 to match existing data format
            for col_name, col_config in config.items():
                if col_config.get('type', '') == 'boolean' and col_name in data_df.columns:
                    # Convert True/False to 1/0
                    data_df[col_name] = data_df[col_name].apply(
                        lambda x: 1 if (x is True or str(x).upper() in ['TRUE', '1', 'YES', 'Y', 'T']) 
                        else (0 if (x is False or str(x).upper() in ['FALSE', '0', 'NO', 'N', 'F'] or pd.isna(x)) else x)
                    )
            
            # Combine config and data
            full_df = pd.concat([config_df, data_df], ignore_index=True)
        else:
            # No config, just save data (but still try to convert booleans if we can detect them)
            # This is a fallback - ideally config should always be provided
            full_df = data_df
        
        conn.update(worksheet=user, data=full_df)
        return True
    except Exception as e:
        error_msg = str(e) if e else "Unknown error"
        error_type = type(e).__name__
        st.error(f"Error saving data for {user}: {error_type} - {error_msg}")
        st.exception(e)
        return False

# App title
st.title("🏆 Bahaha Dilly Dailies")
st.markdown("*<small>(bobby, anne, hansa, anne, harini, anne, vinay with a silent v)</small>*", unsafe_allow_html=True)
st.markdown("### Let's get after 2026, frens!")

# Custom CSS to make selectbox arrow icon bigger on mobile
st.markdown("""
<style>
    /* Make just the dropdown arrow icon 2x bigger */
    .stSelectbox svg {
        transform: scale(2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for user selection
st.sidebar.title("User Login")
users = load_users()
if not users:
    st.sidebar.error("No users found. Please check the 'users' tab in the spreadsheet.")
    st.stop()

# Get user from query parameters (persists across sessions via URL)
query_params = st.query_params
url_user = query_params.get("user", None)

# Validate URL user is in the users list
if url_user and url_user.lower() in [u.lower() for u in users]:
    # Find the exact case match from users list
    default_user = next((u for u in users if u.lower() == url_user.lower()), users[0])
else:
    default_user = users[0]

# Use index to set default
default_index = users.index(default_user) if default_user in users else 0

selected_user = st.sidebar.selectbox("Select your name:", users, index=default_index)

# Update query parameter when user changes
if selected_user != url_user:
    st.query_params["user"] = selected_user

# Load user-specific data and config
if 'current_user' not in st.session_state or st.session_state.current_user != selected_user:
    st.session_state.current_user = selected_user
    st.session_state.df, st.session_state.config = load_user_data(selected_user)
    if st.session_state.config is None:
        st.sidebar.error(f"Could not load configuration for {selected_user}")
        st.stop()

# Ensure we have config loaded (should already be loaded from load_user_data above)
if 'config' not in st.session_state or st.session_state.config is None:
    # This should rarely happen, but if it does, reload
    if 'df' in st.session_state and not st.session_state.df.empty:
        st.session_state.config = load_column_config(selected_user, st.session_state.df)
    else:
        st.session_state.config = load_column_config(selected_user)
    if st.session_state.config is None:
        st.sidebar.error(f"Could not load configuration for {selected_user}")
        st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {selected_user.capitalize()}'s Goals")

# Display user-specific goals in sidebar dynamically
config = st.session_state.config
goals_list = []
for col_name, col_config in config.items():
    if col_config.get('has_goal', False) and col_name not in ['user', 'date', 'notes', 'timestamp']:
        emoji = col_config.get('emoji', '')
        display_name = col_config.get('display_name', col_name)
        units = col_config.get('units', '')
        goal_type = col_config.get('weekly_or_daily_goal', '')
        goal_target = col_config.get('goal_target', '')
        goal_dir = col_config.get('goal_direction', '')
        
        goal_text = f"{emoji} {display_name}"
        if units:
            goal_text += f" ({units})"
        goal_text += ": "
        
        if goal_type == 'daily':
            if isinstance(goal_target, bool) and goal_target:
                goal_text += "Daily"
            elif goal_target:
                if goal_dir == 'at_most':
                    goal_text += f"≤{goal_target} daily"
                else:
                    goal_text += f"≥{goal_target} daily"
        elif goal_type == 'weekly_total':
            if isinstance(goal_target, (int, float)) and goal_target > 0:
                if goal_dir == 'at_most':
                    goal_text += f"≤{goal_target} total/week"
                else:
                    goal_text += f"≥{goal_target} total/week"
            else:
                goal_text += "Weekly total goal"
        elif goal_type == 'count_per_week':
            if isinstance(goal_target, (int, float)) and goal_target > 0:
                if goal_dir == 'at_most':
                    goal_text += f"≤{goal_target} days/week"
                else:
                    goal_text += f"≥{goal_target} days/week"
            else:
                goal_text += "Count per week goal"
        
        goals_list.append(goal_text)

if goals_list:
    st.sidebar.markdown("\n".join([f"- {goal}" for goal in goals_list]))
else:
    st.sidebar.markdown("No goals configured yet.")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📝 Log Today", "📊 My Progress", "😎 Good Looking Week"])

# Helper function to render dynamic form
def render_kpi_form(user, config, existing_data):
    """Render KPI form dynamically based on column configuration"""
    new_entry = {'user': user, 'date': get_tracking_date_str()}
    
    # Separate columns into trackable (not system columns)
    trackable_cols = []
    for col_name, col_config in config.items():
        if col_name not in ['user', 'date', 'notes', 'timestamp']:
            trackable_cols.append((col_name, col_config))
    
    # Split into two columns for layout
    col1, col2 = st.columns(2)
    cols = [col1, col2]
    
    for idx, (col_name, col_config) in enumerate(trackable_cols):
        col = cols[idx % 2]
        col_type = col_config.get('type', 'note')
        emoji = col_config.get('emoji', '')
        display_name = col_config.get('display_name', col_name)
        units = col_config.get('units', '')
        help_text = col_config.get('help_text', '')
        
        # Build label: [emoji] [display_name] ([units])
        label = f"{emoji} {display_name}".strip()
        if units:
            label += f" ({units})"
        
        with col:
            if col_type == 'boolean':
                # Handle 0/1, True/False, and string values
                val = existing_data.get(col_name, False)
                if val in [True, 1, '1', 'TRUE', 'True', 'true']:
                    default_val = True
                elif val in [False, 0, '0', 'FALSE', 'False', 'false'] or pd.isna(val):
                    default_val = False
                else:
                    default_val = bool(val)
                new_entry[col_name] = st.checkbox(
                    label,
                    value=default_val,
                    help=help_text if help_text else None,
                    key=f"checkbox_{user}_{col_name}"
                )
            elif col_type == 'int':
                default_val = int(existing_data.get(col_name, 0)) if existing_data.get(col_name) not in [None, ''] else 0
                new_entry[col_name] = st.number_input(
                    label,
                    min_value=0,
                    max_value=10000,
                    value=default_val,
                    step=1,
                    help=help_text if help_text else None,
                    key=f"number_int_{user}_{col_name}"
                )
            elif col_type == 'float':
                default_val = float(existing_data.get(col_name, 0.0)) if existing_data.get(col_name) not in [None, ''] else 0.0
                new_entry[col_name] = st.number_input(
                    label,
                    min_value=0.0,
                    max_value=10000.0,
                    value=default_val,
                    step=0.1,
                    help=help_text if help_text else None,
                    key=f"number_float_{user}_{col_name}"
                )
            else:  # note or other types - skip for now, handled separately
                # For note types, we'll handle notes separately
                if col_name != 'notes':
                    default_val = existing_data.get(col_name, '')
                    new_entry[col_name] = st.text_input(
                        label,
                        value=str(default_val) if default_val else '',
                        help=help_text if help_text else None,
                        key=f"text_{user}_{col_name}"
                    )
    
    return new_entry

# Tab 1: Log Today's KPIs (Dynamic per user)
with tab1:
    st.header(f"Log KPIs for {selected_user}")

    today = get_tracking_date_str()
    config = st.session_state.config
    df = st.session_state.df

    # Check if already logged today
    if not df.empty and 'date' in df.columns:
        user_data = df[df['date'] == today]
        already_logged = not user_data.empty
        if already_logged:
            st.warning(f"You already logged data for {today}. You can update it below.")
            existing_data = user_data.iloc[0].to_dict()
        else:
            existing_data = {}
    else:
        already_logged = False
        existing_data = {}

    with st.form("kpi_form"):
        st.subheader("Enter your daily metrics:")

        new_entry = render_kpi_form(selected_user, config, existing_data)

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
            if already_logged and not df.empty:
                st.session_state.df = df[df['date'] != today]
            else:
                st.session_state.df = df

            # Add new row
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

            # Save to Google Sheets
            if save_user_data(selected_user, st.session_state.df, config):
                st.success("✅ Data saved successfully!")
                st.balloons()
                # Reload data (TTL cache will refresh on next read)
                st.session_state.df, st.session_state.config = load_user_data(selected_user)
            else:
                st.error("Failed to save to Google Sheets")

# Tab 2: My Progress (Dynamic per user)
with tab2:
    st.header(f"{selected_user.capitalize()}'s Progress")

    user_df = st.session_state.df.copy()
    config = st.session_state.config

    if not user_df.empty and len(user_df) > 0 and 'date' in user_df.columns:
        user_df['date'] = pd.to_datetime(user_df['date'])
        user_df = user_df.sort_values('date')

        # Summary Statistics - averages for all numerical stats (int or float) and boolean counts
        st.subheader("📊 Summary Statistics")

        # Get yesterday's date in US Eastern Time for filtering
        yesterday_et = get_yesterday()
        week_start = yesterday_et - timedelta(days=6)  # 7 days including yesterday
        
        # Filter to past week (ending yesterday)
        user_df['date_only'] = user_df['date'].dt.date
        week_df = user_df[(user_df['date_only'] >= week_start) & (user_df['date_only'] <= yesterday_et)].copy()

        # Get all numerical columns (int or float type) and boolean columns
        numerical_cols = []
        boolean_cols = []
        for col_name, col_config in config.items():
            if col_name not in ['user', 'date', 'notes', 'timestamp']:
                col_type = col_config.get('type', 'note')
                if col_type in ['int', 'float']:
                    numerical_cols.append((col_name, col_config))
                elif col_type == 'boolean':
                    boolean_cols.append((col_name, col_config))
        
        # Combine all columns for display
        all_stats_cols = numerical_cols + boolean_cols
        
        if all_stats_cols:
            # Use 3 columns per row for better spacing
            cols_per_row = 3
            num_rows = (len(all_stats_cols) + cols_per_row - 1) // cols_per_row
            
            for row in range(num_rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    idx = row * cols_per_row + col_idx
                    if idx < len(all_stats_cols):
                        col_name, col_config = all_stats_cols[idx]
                        emoji = col_config.get('emoji', '')
                        display_name = col_config.get('display_name', col_name)
                        units = col_config.get('units', '')
                        col_type = col_config.get('type', 'note')
                        
                        with cols[col_idx]:
                            if col_name in user_df.columns:
                                if col_type in ['int', 'float']:
                                    # Calculate average for past week only
                                    if not week_df.empty and col_name in week_df.columns:
                                        col_data = pd.to_numeric(week_df[col_name], errors='coerce')
                                        col_data_valid = col_data[col_data.notna()]
                                        if len(col_data_valid) > 0:
                                            avg_val = col_data_valid.mean()
                                            # Shorter label
                                            label = f"{emoji} Avg {display_name}"
                                            value_text = f"{avg_val:.1f}"
                                            if units:
                                                value_text += f" {units}"
                                            st.metric(label, value_text)
                                        else:
                                            label = f"{emoji} Avg {display_name}"
                                            value_text = "0.0"
                                            if units:
                                                value_text += f" {units}"
                                            st.metric(label, value_text)
                                    else:
                                        label = f"{emoji} Avg {display_name}"
                                        value_text = "0.0"
                                        if units:
                                            value_text += f" {units}"
                                        st.metric(label, value_text)
                                elif col_type == 'boolean':
                                    # Count non-zero (True) values in past week
                                    if not week_df.empty and col_name in week_df.columns:
                                        # Convert boolean column to numeric for counting
                                        col_data = week_df[col_name].apply(
                                            lambda x: str(x).upper() in ['TRUE', '1', 'YES', 'Y', 'T', True] 
                                            if pd.notna(x) else False
                                        )
                                        true_count = int(col_data.sum())
                                        # Shorter label
                                        label = f"{emoji} {display_name} days"
                                        st.metric(label, f"{true_count}")
                                    else:
                                        label = f"{emoji} {display_name} days"
                                        st.metric(label, "0")
                
                # Add spacing between rows
                if row < num_rows - 1:
                    st.markdown("<br>", unsafe_allow_html=True)

        # Trends section - charts for all numerical stats
        st.subheader("📈 Trends")
        
        if numerical_cols:
            # Display charts in 2 columns
            for idx in range(0, len(numerical_cols), 2):
                cols = st.columns(2)
                for i in range(2):
                    if idx + i < len(numerical_cols):
                        col_name, col_config = numerical_cols[idx + i]
                        emoji = col_config.get('emoji', '')
                        display_name = col_config.get('display_name', col_name)
                        units = col_config.get('units', '')
                        
                        with cols[i]:
                            if col_name in user_df.columns:
                                col_data = pd.to_numeric(user_df[col_name], errors='coerce')
                                if col_data.notna().any():
                                    fig = px.line(user_df, x='date', y=col_name,
                                                title=f"{emoji} {display_name}")
                                    if units:
                                        fig.update_layout(yaxis_title=units)
                                    st.plotly_chart(fig, use_container_width=True)

        # Recent entries
        st.subheader("📅 Recent Entries")
        display_cols = [col for col in user_df.columns if col not in ['user', 'timestamp', 'notes']]
        if display_cols:
            display_df = user_df[display_cols].tail(10).copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_df, use_container_width=True)

    else:
        st.info("No data logged yet. Go to 'Log Today' to start tracking!")

# Helper function to calculate user score dynamically
def calculate_user_score(user, df, config):
    """Calculate user score based on column configuration"""
    if config is None:
        return 0
    
    # Get yesterday's date
    yesterday = get_yesterday()
    
    # Get all columns with goals
    goal_columns = []
    for col_name, col_config in config.items():
        if col_config.get('has_goal', False) and col_name not in ['user', 'date', 'notes', 'timestamp']:
            goal_columns.append((col_name, col_config))
    
    if not goal_columns:
        return 0
    
    # Prepare dataframe if it exists
    if df.empty or 'date' not in df.columns:
        # No data - all goals will be treated as not met (0)
        return 0
    
    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.sort_values('date')
    
    # Filter data to only include entries up to and including yesterday
    df = df[df['date'] <= yesterday].copy()
    
    # Calculate score for each goal
    goal_scores = []
    points_per_goal = 100.0 / len(goal_columns)  # Distribute points evenly
    
    for col_name, col_config in goal_columns:
        goal_type = col_config.get('weekly_or_daily_goal', '')
        goal_target = col_config.get('goal_target', None)
        goal_direction = col_config.get('goal_direction', 'at_least')
        col_type = col_config.get('type', 'note')
        
        if goal_type == 'daily':
            # Daily: Use past 7 days of data (ending yesterday)
            # Compute rate of days with goal met over days with data
            # Score = (M/N) * points_per_goal where M = days met, N = days with data
            # If N=0, score = 0
            
            week_start = yesterday - timedelta(days=6)  # 7 days including yesterday
            
            # Filter to the 7-day period ending yesterday
            week_df = df[(df['date'] >= week_start) & (df['date'] <= yesterday)].copy()
            
            if week_df.empty or col_name not in week_df.columns:
                # No data - N=0, score = 0
                goal_scores.append(0)
                continue
            
            # Get only rows that have data for this column (not NaN)
            week_df_with_data = week_df[week_df[col_name].notna()].copy()
            
            if week_df_with_data.empty:
                # No data for this column - N=0, score = 0
                goal_scores.append(0)
                continue
            
            num_dates_with_data = len(week_df_with_data)  # Number of days with data
            
            # Convert goal_target to numeric
            try:
                if col_type == 'boolean':
                    # For boolean, goal_target should be 1 (True) or 0 (False)
                    goal_target_num = 1 if (goal_target is True or str(goal_target).upper() in ['TRUE', '1']) else 0
                else:
                    goal_target_num = float(goal_target) if goal_target not in [None, '', 'None'] else None
            except (ValueError, TypeError):
                goal_target_num = None
            
            if goal_target_num is None:
                goal_scores.append(0)
                continue
            
            # Count days where goal was met (M)
            num_days_with_goal_met = 0
            for idx, row in week_df_with_data.iterrows():
                value = row[col_name]
                
                # Convert value to numeric (treats boolean as 0/1)
                if col_type == 'boolean':
                    # Convert boolean to 0/1
                    numeric_value = 1 if str(value).upper() in ['TRUE', '1', 'YES', 'Y', 'T', True] else 0
                else:
                    # Convert to numeric
                    try:
                        numeric_value = float(value) if pd.notna(value) else 0
                    except (ValueError, TypeError):
                        numeric_value = 0
                
                # Check if goal was met for this day
                goal_met = False
                if goal_direction == 'at_most':
                    goal_met = numeric_value <= goal_target_num
                else:  # at_least
                    goal_met = numeric_value >= goal_target_num
                
                if goal_met:
                    num_days_with_goal_met += 1
            
            # Calculate score: (M/N) * points_per_goal
            if num_dates_with_data > 0:
                score = (num_days_with_goal_met / num_dates_with_data) * points_per_goal
            else:
                score = 0
            
            goal_scores.append(score)
            
        elif goal_type == 'weekly_total':
            # Weekly total: Sum up values over the preceding 7 days (ending yesterday)
            # Check if total meets goal_threshold
            # If no data, treat as 0
            
            week_start = yesterday - timedelta(days=6)  # 7 days including yesterday
            
            # Filter to the 7-day period ending yesterday
            week_df = df[(df['date'] >= week_start) & (df['date'] <= yesterday)].copy()
            
            if week_df.empty or col_name not in week_df.columns:
                # No data - treat sum as 0
                week_sum = 0
            else:
                # Convert column to numeric (treats boolean as 0/1)
                if col_type == 'boolean':
                    # Convert boolean to 0/1 and sum
                    col_data = week_df[col_name].apply(
                        lambda x: 1 if (pd.notna(x) and str(x).upper() in ['TRUE', '1', 'YES', 'Y', 'T', True]) else 0
                    )
                    week_sum = float(col_data.sum())
                else:
                    # Convert to numeric and sum
                    col_data = pd.to_numeric(week_df[col_name], errors='coerce')
                    week_sum = float(col_data.sum()) if col_data.notna().any() else 0
            
            # Convert goal_target to numeric
            try:
                goal_target_num = float(goal_target) if goal_target not in [None, '', 'None'] else None
            except (ValueError, TypeError):
                goal_target_num = None
            
            if goal_target_num is None:
                goal_scores.append(0)
                continue
            
            # Check if goal was met
            goal_met = False
            if goal_direction == 'at_most':
                goal_met = week_sum <= goal_target_num
            else:  # at_least
                goal_met = week_sum >= goal_target_num
            
            # Weekly portion should still be counted even if there are fewer than 7 data points
            goal_scores.append(points_per_goal if goal_met else 0)
            
        elif goal_type == 'count_per_week':
            # Count per week: Count non-zero values in the 7-day period ending yesterday
            # Check if count meets goal_threshold (at_most or at_least)
            # If no data, treat count as 0
            
            week_start = yesterday - timedelta(days=6)  # 7 days including yesterday
            
            # Filter to the 7-day period ending yesterday
            week_df = df[(df['date'] >= week_start) & (df['date'] <= yesterday)].copy()
            
            if week_df.empty or col_name not in week_df.columns:
                # No data - treat count as 0
                non_zero_count = 0
            else:
                # Count non-zero values (treats boolean True/1 as non-zero)
                if col_type == 'boolean':
                    # Count True/1 values
                    col_data = week_df[col_name].apply(
                        lambda x: 1 if (pd.notna(x) and str(x).upper() in ['TRUE', '1', 'YES', 'Y', 'T', True]) else 0
                    )
                    non_zero_count = int(col_data.sum())
                else:
                    # Convert to numeric and count non-zero values
                    col_data = pd.to_numeric(week_df[col_name], errors='coerce')
                    # Count values that are not NaN and not zero
                    non_zero_count = int((col_data.notna() & (col_data != 0)).sum())
            
            # Convert goal_target to numeric
            try:
                goal_target_num = float(goal_target) if goal_target not in [None, '', 'None'] else None
            except (ValueError, TypeError):
                goal_target_num = None
            
            if goal_target_num is None:
                goal_scores.append(0)
                continue
            
            # Check if goal was met
            goal_met = False
            if goal_direction == 'at_most':
                goal_met = non_zero_count <= goal_target_num
            else:  # at_least
                goal_met = non_zero_count >= goal_target_num
            
            # Count per week should still be counted even if there are fewer than 7 data points
            goal_scores.append(points_per_goal if goal_met else 0)
    
    return sum(goal_scores)

# Tab 3: Good Looking Week
with tab3:
    st.header("😎 Good Looking Weeks")

    st.info("💡 Who's having a good looking week? Scores are based on each person's individual goals and completion rates.")

    leaderboard_data = []

    # Load all users' data in a single cached batch operation
    all_users_data = load_all_users_data(users)

    for user in users:
        user_specific_df, user_config = all_users_data.get(user, (pd.DataFrame(), None))

        if user_specific_df.empty or len(user_specific_df) == 0 or user_config is None:
            continue

        total_days = len(user_specific_df)

        # Calculate score dynamically based on column configuration
        score = calculate_user_score(user, user_specific_df, user_config)

        leaderboard_data.append({
            'User': user.capitalize(),
            'Total Days': total_days,
            'Score': round(score, 1)
        })

    if leaderboard_data:
        # Create leaderboard DataFrame
        lb_df = pd.DataFrame(leaderboard_data)
        lb_df = lb_df.sort_values('Score', ascending=False).reset_index(drop=True)
        lb_df.index = lb_df.index + 1

        # Display podium
        st.subheader("🏅 This Week's Vibes")
        cols = st.columns(len(lb_df))
        medals = ['🥇', '🥈', '🥉', '🏅', '🏅']

        for idx, (i, row) in enumerate(lb_df.iterrows()):
            with cols[idx]:
                medal = medals[idx] if idx < len(medals) else '🏅'
                st.markdown(f"### {medal} #{i}")
                st.markdown(f"### {row['User']}")
                st.metric("Score", f"{row['Score']:.1f}/100")
                st.caption(f"{row['Total Days']} days logged")

        # Detailed view
        st.subheader("📊 Detailed View")
        st.dataframe(lb_df, use_container_width=True)

        st.caption("""
        **Scoring System**: Each person is scored out of 100 based on their individual goals.
        Scores reflect what percentage of personal goals were met across all logged days in the preceding week.
        """)

    else:
        st.info("No data available yet. Start logging to see who's having a good looking week!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for tracking daily progress | 🏆 Happy New Year!!")

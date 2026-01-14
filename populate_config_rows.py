"""
Script to populate configuration rows (2-10) in each user's tab based on old USER_CONFIG.
Run this once to migrate from hardcoded config to spreadsheet-based config.
"""

# Reconstructed USER_CONFIG from old code
OLD_CONFIG = {
    "bobby": {
        "columns": ['user', 'date', 'strength_workout', 'pt_mobility', 'eating_enough', 'rhr', 'vo2max', 'play_with_sony', 'hrv', 'notes', 'timestamp'],
        "weekly_goals": {'strength_workout': 3},
        "daily_goals": {'pt_mobility': True, 'eating_enough': True, 'play_with_sony': True},
        "display_names": {
            'user': 'User', 'date': 'Date', 'strength_workout': 'Strength Workout', 
            'pt_mobility': 'PT/Mobility', 'eating_enough': 'Eating Enough', 
            'rhr': 'Resting Heart Rate', 'vo2max': 'VO2 Max', 
            'play_with_sony': 'Play with Sony', 'hrv': 'HRV', 
            'notes': 'Notes', 'timestamp': 'Timestamp'
        },
        "emojis": {
            'user': '👤', 'date': '📅', 'strength_workout': '💪', 
            'pt_mobility': '🧘', 'eating_enough': '🍽️', 
            'rhr': '❤️', 'vo2max': '🫁', 
            'play_with_sony': '🐱', 'hrv': '📊', 
            'notes': '📝', 'timestamp': '⏰'
        },
        "units": {
            'rhr': 'bpm', 'vo2max': '', 'hrv': ''
        },
        "types": {
            'user': 'note', 'date': 'date', 'strength_workout': 'boolean',
            'pt_mobility': 'boolean', 'eating_enough': 'boolean', 
            'rhr': 'int', 'vo2max': 'float', 'play_with_sony': 'boolean',
            'hrv': 'int', 'notes': 'note', 'timestamp': 'timestamp'
        },
        "help_texts": {
            'strength_workout': 'Goal: 3x per week',
            'pt_mobility': 'Daily goal',
            'eating_enough': 'Daily goal',
            'play_with_sony': 'Daily goal: 5 minutes',
            'rhr': 'Optional tracking',
            'vo2max': 'Optional tracking',
            'hrv': 'Heart Rate Variability'
        }
    },
    "hansa": {
        "columns": ['user', 'date', 'strength_workout', 'mobility', 'glute_exercises', 'cardio', 'added_sugar', 'notes', 'timestamp'],
        "weekly_goals": {'strength_workout': 2, 'glute_exercises': 2, 'cardio': 4},
        "daily_goals": {'mobility': True, 'added_sugar': 25},
        "display_names": {
            'user': 'User', 'date': 'Date', 'strength_workout': 'Strength Workout',
            'mobility': 'Mobility', 'glute_exercises': 'Glute Exercises',
            'cardio': 'Cardio', 'added_sugar': 'Added Sugar',
            'notes': 'Notes', 'timestamp': 'Timestamp'
        },
        "emojis": {
            'user': '👤', 'date': '📅', 'strength_workout': '💪',
            'mobility': '🧘', 'glute_exercises': '🍑',
            'cardio': '🏃', 'added_sugar': '🍬',
            'notes': '📝', 'timestamp': '⏰'
        },
        "units": {
            'added_sugar': 'grams'
        },
        "types": {
            'user': 'note', 'date': 'date', 'strength_workout': 'boolean',
            'mobility': 'boolean', 'glute_exercises': 'boolean',
            'cardio': 'boolean', 'added_sugar': 'int',
            'notes': 'note', 'timestamp': 'timestamp'
        },
        "help_texts": {
            'strength_workout': 'Goal: 2x per week',
            'mobility': 'Daily goal',
            'glute_exercises': 'Goal: 2x per week',
            'cardio': 'Goal: 4x per week',
            'added_sugar': 'Goal: Less than 25g daily'
        }
    },
    "anne": {
        "columns": ['user', 'date', 'sleep_rested', 'knee_pt_minutes', 'back_pt_minutes', 'protein', 'water',
                   'cardio_minutes', 'push_strength_minutes', 'pull_strength_minutes', 'good_mental_health_day', 'notes', 'timestamp'],
        "weekly_goals": {'cardio_minutes': 4, 'push_strength_minutes': 2, 'pull_strength_minutes': 2},
        "daily_goals": {'sleep_rested': True, 'knee_pt_minutes': True, 'back_pt_minutes': True,
                       'protein': 100, 'water': 80},
        "display_names": {
            'user': 'User', 'date': 'Date', 'sleep_rested': 'Woke Up Feeling Rested',
            'knee_pt_minutes': 'Knee PT', 'back_pt_minutes': 'Back PT',
            'protein': 'Protein', 'water': 'Water',
            'cardio_minutes': 'Cardio', 'push_strength_minutes': 'Push Strength',
            'pull_strength_minutes': 'Pull Strength', 'good_mental_health_day': 'Good Mental Health Today',
            'notes': 'Notes', 'timestamp': 'Timestamp'
        },
        "emojis": {
            'user': '👤', 'date': '📅', 'sleep_rested': '💤',
            'knee_pt_minutes': '🦵', 'back_pt_minutes': '🧘',
            'protein': '🥩', 'water': '💧',
            'cardio_minutes': '🏃', 'push_strength_minutes': '💪',
            'pull_strength_minutes': '💪', 'good_mental_health_day': '🧠',
            'notes': '📝', 'timestamp': '⏰'
        },
        "units": {
            'knee_pt_minutes': 'minutes', 'back_pt_minutes': 'minutes',
            'protein': 'grams', 'water': 'oz',
            'cardio_minutes': 'minutes', 'push_strength_minutes': 'minutes',
            'pull_strength_minutes': 'minutes'
        },
        "types": {
            'user': 'note', 'date': 'date', 'sleep_rested': 'boolean',
            'knee_pt_minutes': 'int', 'back_pt_minutes': 'int',
            'protein': 'int', 'water': 'int',
            'cardio_minutes': 'int', 'push_strength_minutes': 'int',
            'pull_strength_minutes': 'int', 'good_mental_health_day': 'boolean',
            'notes': 'note', 'timestamp': 'timestamp'
        },
        "help_texts": {
            'knee_pt_minutes': 'Daily goal',
            'back_pt_minutes': 'Daily goal',
            'protein': 'Goal: 100g daily',
            'water': 'Goal: 80oz daily',
            'cardio_minutes': 'Goal: 4x per week',
            'push_strength_minutes': 'Goal: 2x per week | Chest, shoulders, triceps, quads',
            'pull_strength_minutes': 'Goal: 2x per week | Lats, biceps, hamstrings, glutes',
            'good_mental_health_day': "Check if you're having a good mental health day"
        }
    },
    "vinay": {
        "columns": ['user', 'date', 'sleep_hours', 'drinks_daily', 'pt_minutes', 'red_meat',
                   'strength_workout', 'workout_minutes', 'saw_anne', 'notes', 'timestamp'],
        "weekly_goals": {'strength_workout': 2, 'drinks_daily': 12, 'red_meat': 7},
        "daily_goals": {'drinks_daily': 2, 'pt_minutes': True, 'workout_minutes': True},
        "display_names": {
            'user': 'User', 'date': 'Date', 'sleep_hours': 'Sleep',
            'drinks_daily': 'Drinks Today', 'pt_minutes': 'PT',
            'red_meat': 'Red Meat Today', 'strength_workout': 'Strength Workout Today',
            'workout_minutes': 'Total Workout', 'saw_anne': 'Times Saw Anne',
            'notes': 'Notes', 'timestamp': 'Timestamp'
        },
        "emojis": {
            'user': '👤', 'date': '📅', 'sleep_hours': '💤',
            'drinks_daily': '🍺', 'pt_minutes': '🧘',
            'red_meat': '🥩', 'strength_workout': '💪',
            'workout_minutes': '🏃', 'saw_anne': '👀',
            'notes': '📝', 'timestamp': '⏰'
        },
        "units": {
            'sleep_hours': 'hours', 'pt_minutes': 'minutes',
            'workout_minutes': 'minutes'
        },
        "types": {
            'user': 'note', 'date': 'date', 'sleep_hours': 'float',
            'drinks_daily': 'int', 'pt_minutes': 'int',
            'red_meat': 'boolean', 'strength_workout': 'boolean',
            'workout_minutes': 'int', 'saw_anne': 'int',
            'notes': 'note', 'timestamp': 'timestamp'
        },
        "help_texts": {
            'drinks_daily': 'Goal: 2 daily max, 12 weekly max',
            'pt_minutes': 'Daily goal',
            'red_meat': 'Track daily and weekly consumption',
            'strength_workout': 'Goal: 2x per week',
            'workout_minutes': 'Daily workout minutes',
            'saw_anne': 'Track how many times you saw Anne today'
        }
    },
    "harini": {
        "columns": ['user', 'date', 'screen_time_minutes', 'yoga', 'strength_workout',
                   'outdoor_walking_minutes', 'notes', 'timestamp'],
        "weekly_goals": {'yoga': 2, 'strength_workout': 2},
        "daily_goals": {'outdoor_walking_minutes': True},
        "display_names": {
            'user': 'User', 'date': 'Date', 'screen_time_minutes': 'Screen Time',
            'yoga': 'Yoga Done', 'strength_workout': 'Strength Workout Done',
            'outdoor_walking_minutes': 'Outdoor Walking',
            'notes': 'Notes', 'timestamp': 'Timestamp'
        },
        "emojis": {
            'user': '👤', 'date': '📅', 'screen_time_minutes': '📱',
            'yoga': '🧘', 'strength_workout': '💪',
            'outdoor_walking_minutes': '🌳',
            'notes': '📝', 'timestamp': '⏰'
        },
        "units": {
            'screen_time_minutes': 'minutes', 'outdoor_walking_minutes': 'minutes'
        },
        "types": {
            'user': 'note', 'date': 'date', 'screen_time_minutes': 'int',
            'yoga': 'boolean', 'strength_workout': 'boolean',
            'outdoor_walking_minutes': 'int',
            'notes': 'note', 'timestamp': 'timestamp'
        },
        "help_texts": {
            'screen_time_minutes': 'Track daily screen time',
            'yoga': 'Goal: 2x per week',
            'strength_workout': 'Goal: 2x per week',
            'outdoor_walking_minutes': 'Daily outdoor walking'
        }
    }
}

def populate_config_rows():
    """Populate configuration rows 2-10 for each user tab"""
    # Read secrets.toml manually (simple TOML parser for our use case)
    try:
        secrets = {}
        with open('.streamlit/secrets.toml', 'r') as f:
            content = f.read()
            # Simple parsing for our specific format
            import re
            # Extract spreadsheet URL
            spreadsheet_match = re.search(r'spreadsheet\s*=\s*"([^"]+)"', content)
            spreadsheet_url = spreadsheet_match.group(1) if spreadsheet_match else None
            
            # Extract other fields
            conn_config = {}
            for key in ['project_id', 'private_key_id', 'private_key', 'client_email', 
                       'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url', 
                       'client_x509_cert_url']:
                if key == 'private_key':
                    # Handle multiline private key
                    match = re.search(r'private_key\s*=\s*"""([^"]+(?:"[^"]*"[^"]*)*)"""', content, re.DOTALL)
                    if match:
                        conn_config[key] = match.group(1)
                    else:
                        match = re.search(r'private_key\s*=\s*"([^"]+)"', content)
                        conn_config[key] = match.group(1).replace('\\n', '\n') if match else ''
                else:
                    match = re.search(rf'{key}\s*=\s*"([^"]+)"', content)
                    conn_config[key] = match.group(1) if match else ''
            
            conn_config['spreadsheet'] = spreadsheet_url
    except Exception as e:
        print(f"Could not read secrets.toml: {e}")
        print("Make sure .streamlit/secrets.toml exists and is properly formatted.")
        return
    
    # Use gspread directly
    import gspread
    from google.oauth2.service_account import Credentials
    
    # Build credentials from config
    creds_info = {
        'type': 'service_account',
        'project_id': conn_config.get('project_id'),
        'private_key_id': conn_config.get('private_key_id'),
        'private_key': conn_config.get('private_key', '').replace('\\n', '\n'),
        'client_email': conn_config.get('client_email'),
        'client_id': conn_config.get('client_id'),
        'auth_uri': conn_config.get('auth_uri', 'https://accounts.google.com/o/oauth2/auth'),
        'token_uri': conn_config.get('token_uri', 'https://oauth2.googleapis.com/token'),
        'auth_provider_x509_cert_url': conn_config.get('auth_provider_x509_cert_url', 'https://www.googleapis.com/oauth2/v1/certs'),
        'client_x509_cert_url': conn_config.get('client_x509_cert_url'),
    }
    
    try:
        creds = Credentials.from_service_account_info(creds_info, scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ])
        
        client = gspread.authorize(creds)
        spreadsheet_url = conn_config.get('spreadsheet')
        if not spreadsheet_url:
            print("Error: No spreadsheet URL found in secrets.toml")
            return
        sheet_id = spreadsheet_url.split('/d/')[1].split('/')[0]
        spreadsheet = client.open_by_key(sheet_id)
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return
    
    for user, config in OLD_CONFIG.items():
        print(f"\nProcessing {user}...")
        try:
            worksheet = spreadsheet.worksheet(user)
            
            # Get all existing data
            all_values = worksheet.get_all_values()
            if not all_values:
                print(f"  Warning: No data found in {user} tab")
                continue
            
            # Get column names from row 1
            row1 = all_values[0] if all_values else []
            if not row1:
                print(f"  Warning: No columns found in row 1 for {user}")
                continue
            
            columns = row1
            
            # Check if config rows already exist (rows 2-10 should have config names in column A)
            has_existing_config = False
            if len(all_values) >= 10:
                # Check if row 2 has a config name in column A
                if len(all_values) > 1 and all_values[1] and all_values[1][0] in ['display_name', 'emoji', 'units', 'type', 'has_goal', 'weekly_or_daily_goal', 'goal_target', 'goal_direction', 'help_text']:
                    has_existing_config = True
                    print(f"  Note: Config rows already exist, will update them")
            
            # If config rows don't exist, shift existing data down
            if not has_existing_config:
                # Get existing data rows (everything after row 1)
                existing_data = all_values[1:] if len(all_values) > 1 else []
                
                if existing_data:
                    print(f"  Shifting {len(existing_data)} existing data rows down by 9 rows...")
                    # Clear the worksheet first (we'll rebuild it)
                    worksheet.clear()
                    
                    # Write row 1 (column names) back
                    worksheet.update(values=[row1], range_name='A1')
                    
                    # Write existing data starting at row 11
                    if existing_data:
                        worksheet.update(values=existing_data, range_name='A11')
            
            # Build config rows with config names in column A
            config_row_names = ['display_name', 'emoji', 'units', 'type', 'has_goal', 
                              'weekly_or_daily_goal', 'goal_target', 'goal_direction', 'help_text']
            config_rows = []
            
            # Row 2: display_name
            row2 = [config_row_names[0]] + [config['display_names'].get(col, col.title().replace('_', ' ')) for col in columns[1:]]
            config_rows.append(row2)
            
            # Row 3: emoji
            row3 = [config_row_names[1]] + [config['emojis'].get(col, '') for col in columns[1:]]
            config_rows.append(row3)
            
            # Row 4: units
            row4 = [config_row_names[2]] + [config['units'].get(col, '') for col in columns[1:]]
            config_rows.append(row4)
            
            # Row 5: type
            row5 = [config_row_names[3]] + [config['types'].get(col, 'note') for col in columns[1:]]
            config_rows.append(row5)
            
            # Row 6: has_goal
            row6 = [config_row_names[4]]
            for col in columns[1:]:
                has_goal = col in config['weekly_goals'] or col in config['daily_goals']
                row6.append('TRUE' if has_goal else 'FALSE')
            config_rows.append(row6)
            
            # Row 7: weekly_or_daily_goal
            row7 = [config_row_names[5]]
            for col in columns[1:]:
                if col in config['weekly_goals']:
                    row7.append('weekly')
                elif col in config['daily_goals']:
                    row7.append('daily')
                else:
                    row7.append('')
            config_rows.append(row7)
            
            # Row 8: goal_target
            row8 = [config_row_names[6]]
            for col in columns[1:]:
                if col in config['weekly_goals']:
                    row8.append(config['weekly_goals'][col])
                elif col in config['daily_goals']:
                    row8.append(config['daily_goals'][col])
                else:
                    row8.append('')
            config_rows.append(row8)
            
            # Row 9: goal_direction
            row9 = [config_row_names[7]]
            for col in columns[1:]:
                if col in config['daily_goals'] and isinstance(config['daily_goals'][col], (int, float)):
                    # For numeric daily goals, check if it's a "less than" goal
                    if col == 'added_sugar':  # Special case: less than 25g
                        row9.append('at_most')
                    else:
                        row9.append('at_least')
                elif col in config['weekly_goals'] and isinstance(config['weekly_goals'][col], (int, float)):
                    # For weekly goals, check if it's a max (like drinks_daily: 12)
                    if col == 'drinks_daily' or col == 'red_meat':  # Special cases
                        row9.append('at_most')
                    else:
                        row9.append('at_least')
                else:
                    row9.append('at_least')  # Default for boolean goals
            config_rows.append(row9)
            
            # Row 10: help_text
            row10 = [config_row_names[8]] + [config['help_texts'].get(col, '') for col in columns[1:]]
            config_rows.append(row10)
            
            # Write rows 2-10 (indices 1-9 in 0-indexed, but gspread uses 1-indexed)
            for idx, row_data in enumerate(config_rows, start=2):
                # Ensure row_data has same length as columns
                while len(row_data) < len(columns):
                    row_data.append('')
                # Use correct parameter order to avoid deprecation warning
                worksheet.update(values=[row_data[:len(columns)]], range_name=f'A{idx}')
            
            print(f"  ✓ Successfully populated config rows for {user}")
            
        except Exception as e:
            print(f"  ✗ Error processing {user}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Populating configuration rows in Google Sheets...")
    print("=" * 60)
    populate_config_rows()
    print("=" * 60)
    print("Done!")

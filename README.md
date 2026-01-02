# 🏆 Bahaha Dilly Dailies
*(bobby, anne, hansa, anne, harini, anne, vinay with a silent v)*

A personal KPI tracking app for five friends with completely customized goals and metrics

## Features

- **📝 Daily Logging**: Each person tracks their own personalized KPIs:
  - **Bobby**: Strength workouts, PT/mobility, eating enough, RHR, VO2max
  - **Hansa**: Strength, mobility, glute exercises, cardio, added sugar
  - **Anne**: Sleep quality, knee/back PT, protein, water, cardio, push/pull strength, mental health
  - **Vinay**: Sleep hours, drinks, PT, red meat, strength, workout minutes
  - **Harini**: Screen time, yoga, strength, outdoor walking

- **📊 Personal Progress**: View your individual trends, charts, and statistics based on your custom goals
- **😎 Good Looking Weeks**: See who's having a good looking week! Scores based on each person's individual goal completion
- **☁️ Cloud Storage**: All data saved to Google Sheets in separate tabs for each person
- **🔄 Real-time Sync**: Everyone sees the same data instantly

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Cloud account (free)
- Access to the shared Google Sheet

### Installation

1. Clone or download this repository:
```bash
git clone https://github.com/HelloAnneKim/bahaha-dilly-dailies.git
cd bahaha-dilly-dailies
```

2. Install required dependencies:
```bash
pip3 install -r requirements.txt
```

3. **Set up Google Sheets API (REQUIRED)**:
   - Follow the detailed instructions in [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)
   - This is a one-time setup to connect the app to your shared Google Sheet
   - You'll need to create a service account and download `credentials.json`

### Running the App

Start the Streamlit app with:
```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### Google Sheet Setup

**IMPORTANT**: Your Google Sheet must have **5 separate tabs** named exactly:
- `anne`
- `bobby`
- `hansa`
- `vinay`
- `harini`

Each person's data will be stored in their own tab with their custom columns.

## How to Use

### Logging Daily KPIs

1. Select your name from the sidebar dropdown
2. Go to the "📝 Log Today" tab
3. Enter your personalized metrics for the day (each person has different fields based on their goals)
4. Click "💾 Save Today's Data"

### Viewing Progress

- **📊 My Progress**: See your personal trends, charts, and statistics customized for your goals
- **😎 Good Looking Weeks**: See who's having a good looking week based on goal completion rates

## Scoring System

Each person is scored out of 100 based on their individual goals. The scoring reflects what percentage of personal daily and weekly goals were met across all logged days. Since everyone has different goals, this ensures fair comparison!

## Data Storage

All data is stored in **Google Sheets** with separate tabs for each person!

**Spreadsheet URL**: https://docs.google.com/spreadsheets/d/1XcW5S3flYiSkOBhxCyJ0VuZGWp462Oa8Eah6LnlAU1U/edit

### How It Works

- Each person has their own tab in the Google Sheet (anne, bobby, hansa, vinay, harini)
- When anyone saves data, it's immediately written to their tab in the Google Sheet
- Everyone running the app sees the same shared data in real-time
- You can view/edit data directly in Google Sheets if needed
- Each tab has different columns based on that person's custom KPIs
- No need to sync files or worry about conflicts!

### Benefits

- ✅ Real-time collaboration
- ✅ No manual syncing required
- ✅ Data accessible from anywhere
- ✅ Can view/edit directly in Google Sheets
- ✅ Automatic backups through Google

## Git Setup (Optional)

To version control your data and share via GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Troubleshooting

**App won't start**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

**Data not saving**: Check that the app has write permissions in the current directory

**Port already in use**: Stop other Streamlit apps or specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## Future Enhancements

Potential features to add:
- [ ] Weekly/monthly challenges
- [ ] Achievement badges
- [ ] Photo uploads for meals
- [ ] Export data to CSV
- [ ] Mobile-responsive design improvements
- [ ] Dark mode
- [ ] Notifications/reminders
- [ ] Weekly summaries and insights

## Contributing

Feel free to fork this repo and add your own features! Some ideas:
- Add more personalized KPI types for each person
- Improve the scoring algorithm
- Add more visualization options
- Create weekly/monthly summary views

## License

Free to use and modify for personal use!

---

Made with ❤️ for tracking daily progress | Happy New Year!!
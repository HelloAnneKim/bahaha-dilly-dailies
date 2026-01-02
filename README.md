# 🏆 bahaha+v dilly dailies

A personal kpi tracking app for a couple of friendos

## Features

- **📝 Daily Logging**: Log your daily KPIs including:
  - 💤 Sleep (hours)
  - 🏃 Exercise completion
  - 💪 PT quota completion
  - 💧 Water intake (oz)
  - 🥩 Protein intake (grams)
  etc etc etc

- **📊 Personal Progress**: View your individual trends and statistics
- **🏆 Leaderboard**: Encourage friends as they complete their weekly/daily goals
- **📈 Group Analytics**: Compare metrics across all users
- **☁️ Cloud Storage**: All data saved to Google Sheets for real-time sharing
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

### Customizing User Names

To change the default user names ("Friend 1", "Friend 2", "Friend 3"):

1. Open `app.py` in a text editor
2. Find this line (around line 38):
```python
users = ["Friend 1", "Friend 2", "Friend 3"]
```
3. Replace with your actual names:
```python
users = ["Alice", "Bob", "Charlie"]
```
4. Save the file and restart the app

## How to Use

### Logging Daily KPIs

1. Select your name from the sidebar dropdown
2. Go to the "📝 Log Today" tab
3. Enter your metrics for the day
4. Click "💾 Save Today's Data"

### Viewing Progress

- **My Progress**: See your personal trends, charts, and statistics
- **Leaderboard**: View rankings and see who's winning
- **Analytics**: Compare metrics across all users with detailed charts

## Scoring System

The leaderboard uses a scoring system of percentage of daily and weekly goals completed.

## Data Storage

All data is stored in **Google Sheets** for real-time sharing between all users!

**Spreadsheet URL**: https://docs.google.com/spreadsheets/d/1XcW5S3flYiSkOBhxCyJ0VuZGWp462Oa8Eah6LnlAU1U/edit

### How It Works

- When anyone saves data, it's immediately written to the Google Sheet
- Everyone running the app sees the same shared data
- You can view/edit data directly in Google Sheets if needed
- All five friends (anne, bobby, hansa, vinay, harini) share the same dataset but separated in different google sheet tabs of the same
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
- [ ] Custom KPI targets per user
- [ ] Photo uploads for meals
- [ ] Export data to CSV
- [ ] Mobile-responsive design improvements
- [ ] Dark mode
- [ ] Notifications/reminders

## Contributing

Feel free to fork this repo and add your own features! Some ideas:
- Add more KPI types
- Improve the scoring algorithm
- Create different leaderboard views
- Add data visualization options

## License

Free to use and modify for personal use!

---

Made with ❤️ for tracking daily progress | Happy New Year!!
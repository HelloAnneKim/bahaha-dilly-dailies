# 🏆 Bahaha Dilly Dailies

A fun and competitive daily KPI tracking app for you and your friends! Track sleep, exercise, PT quotas, water intake, and protein consumption while competing on a leaderboard.

## Features

- **📝 Daily Logging**: Log your daily KPIs including:
  - 💤 Sleep (hours)
  - 🏃 Exercise completion
  - 💪 PT quota completion
  - 💧 Water intake (oz)
  - 🥩 Protein intake (grams)

- **📊 Personal Progress**: View your individual trends and statistics
- **🏆 Leaderboard**: Compete with friends and see who's crushing it
- **📈 Group Analytics**: Compare metrics across all users
- **💾 Data Persistence**: All data saved locally in JSON format

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository:
```bash
git clone <your-repo-url>
cd bahaha-dilly-dailies
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

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

The leaderboard uses a weighted scoring system:
- Sleep goal met (≥8 hours): 10 points per day
- Exercise completed: 15 points per day
- PT quota completed: 15 points per day
- Average water intake: bonus points
- Average protein intake: bonus points

## Data Storage

All data is stored in `kpi_data.json` in the same directory as the app. This file is automatically created when you first save data.

### Sharing Data with Friends

Since data is stored locally, here are options for sharing:

#### Option 1: Shared Computer
Run the app on a shared computer where all friends can access it.

#### Option 2: GitHub Sync
1. Initialize a git repository (see below)
2. Each person pulls the latest `kpi_data.json` before logging
3. After logging, commit and push the updated `kpi_data.json`
4. Other friends pull the updates

#### Option 3: Cloud Storage
Keep `kpi_data.json` in a shared folder (Dropbox, Google Drive, etc.) and run the app from there.

#### Option 4: Deploy to Cloud (Advanced)
Deploy to Streamlit Community Cloud, Heroku, or other hosting service. You'll need to add a proper database for multi-user concurrent access.

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

Made with ❤️ for tracking daily progress | Keep grinding! 💪

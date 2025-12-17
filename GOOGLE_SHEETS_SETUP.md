# Google Sheets Setup Guide

This app now uses Google Sheets as the backend database! This allows all three friends to share data in real-time.

## Spreadsheet URL
https://docs.google.com/spreadsheets/d/1XcW5S3flYiSkOBhxCyJ0VuZGWp462Oa8Eah6LnlAU1U/edit

## Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Bahaha Dilly Dailies" and click "Create"

### Step 2: Enable Google Sheets API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"
4. Also search for "Google Drive API" and enable it

### Step 3: Create Service Account Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name it "bahaha-dailies-bot" (or any name you like)
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

### Step 4: Generate JSON Key

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create" - a JSON file will download

### Step 5: Add Credentials to Your Project

1. Rename the downloaded file to `credentials.json`
2. Move it to your `bahaha-dilly-dailies` folder (same folder as `app.py`)

### Step 6: Share Google Sheet with Service Account

1. Open the downloaded `credentials.json` file
2. Find the `client_email` field - it looks like: `bahaha-dailies-bot@your-project.iam.gserviceaccount.com`
3. Copy this email address
4. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1XcW5S3flYiSkOBhxCyJ0VuZGWp462Oa8Eah6LnlAU1U/edit
5. Click "Share" button
6. Paste the service account email
7. Give it "Editor" access
8. Uncheck "Notify people"
9. Click "Share"

### Step 7: Install Dependencies and Run

```bash
pip3 install -r requirements.txt
python3 -m streamlit run app.py
```

## Security Notes

**IMPORTANT:**
- **DO NOT** commit `credentials.json` to GitHub
- It's already in `.gitignore` to prevent accidental commits
- Anyone with this file can access your Google Sheet

## Troubleshooting

### Error: "credentials.json not found"
- Make sure the file is named exactly `credentials.json`
- Make sure it's in the same folder as `app.py`

### Error: "Permission denied"
- Make sure you shared the spreadsheet with the service account email
- Make sure you gave it "Editor" access, not just "Viewer"

### Error: "API not enabled"
- Make sure both Google Sheets API and Google Drive API are enabled in your Google Cloud project

## How It Works

- When you save data in the app, it writes to the Google Sheet
- All three friends can run the app and see the same shared data
- The Google Sheet acts as your shared database
- You can also view/edit the data directly in Google Sheets if needed

## Alternative: Using Streamlit Secrets (for deployment)

If you want to deploy this to Streamlit Cloud:

1. Don't add `credentials.json` to the repo
2. Instead, add the credentials to Streamlit secrets
3. Follow Streamlit's guide: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

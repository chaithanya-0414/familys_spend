# Deployment Guide for Streamlit

## 1. Run Locally
To run the app on your computer:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

## 2. Deploy to Streamlit Cloud (Free & Easy)
Streamlit Community Cloud is the easiest way to host this for free.

1.  **Push to GitHub**: Make sure this folder is a GitHub repository.
    ```bash
    git init
    git add .
    git commit -m "Initial Streamlit App"
    # (Then push to your remote repo)
    ```
2.  **Sign up/Login**: Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3.  **New App**: Click "New app".
4.  **Select Repo**: Choose your repository, branch (usually `main`), and the file path `streamlit_app.py`.
5.  **Deploy**: Click "Deploy!".

The app will be live in minutes.

## 3. Persistent Data (Google Sheets Setup)
**Crucial**: To make sure your data is saved forever (and not lost when the app restarts), we have switched the app to use **Google Sheets**.

### Step 1: Create a Google Cloud Service Account
1.  Go to **[Google Cloud Console](https://console.cloud.google.com/)**.
2.  Create a New Project (e.g., "FamilySpend").
3.  Enable **Google Sheets API**.
4.  Go to **IAM & Admin > Service Accounts** and create a service account.
5.  Create a **JSON Key** for this account and download it.
6.  **Copy the email address** of the service account (it looks like `name@project.iam.gserviceaccount.com`).

### Step 2: Create your Spreadsheet
1.  Create a new empty Google Sheet at [sheets.new](https://sheets.new).
2.  Name it "FamilySpend Data".
3.  Click **Share** and paste the **Service Account Email** (from step 1). Give it **Editor** access.
4.  Copy the URL of the sheet.

### Step 3: Configure Secrets on Streamlit Cloud
1.  Go to your app on [share.streamlit.io](https://share.streamlit.io/).
2.  Click the **Settings** (three dots) -> **Settings** -> **Secrets**.
3.  Paste the following configuration (using your Sheet URL and the contents of your JSON key file):

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

# Paste the contents of your JSON key file below
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

### Step 4: Reboot App
Once secrets are saved, click **Reboot App**. Your app will now read/write to your private Google Sheet!

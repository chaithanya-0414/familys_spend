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

## 3. Persistent Data
**Important**: By default, Streamlit Cloud will reset your SQLite database (`data.db`) every time the app restarts or redeploys.
For permanent storage, you should switch to a cloud database (like Google Sheets, Supabase, or Neon Postgres).

**For now (Simple Start):**
- The SQLite file is good for testing.
- If you restart the app on the cloud, data might be lost.

**Recommended Upgrade for Real Usage**:
- Use **Streamlit Sheets Connection** to store data in a private Google Sheet. It's free and persistent.

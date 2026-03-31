# 🚀 Quick Deployment Guide: Streamlit Community Cloud

Your AI Resume Analyzer is 100% ready to be deployed for free on Streamlit Community Cloud! Follow these simple steps:

## Step 1: Upload to GitHub
1. Go to [GitHub.com](https://github.com/) and create a new repository (e.g., `ai-resume-analyzer`).
2. Upload all the files from this folder (`d:\AI_RESUME_ANALYZER`) into the repository.
   *Make sure `app.py`, `requirements.txt`, and your folders (`core`, `matching`, `pages`, `vectordb`, `assets`) are in the root of the repository.*
3. **Do not** upload the `.env` file or your `venv` folder! (They contain your private API keys).

## Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New app"**.
3. Select your new GitHub repository (`ai-resume-analyzer`).
4. Set the **Main file path** to `app.py`.
5. **DO NOT CLICK DEPLOY YET!** You need to add your API keys first.

## Step 3: Add Your Secrets (API Keys)
1. Before clicking deploy, click on **"Advanced settings..."** (or "Secrets" if you are in the app dashboard).
2. Look for the **Secrets** text box.
3. Paste the following configuration, replacing the `...` with your actual API keys:

```toml
GROQ_API_KEY = "gsk_..."
PINECONE_API_KEY = "pcsk_..."
PINECONE_INDEX_NAME = "resume-analyzer-free"
LANGCHAIN_TRACING_V2 = "false"
```
4. Click **Save**.

## Step 4: Launch!
1. Click **Deploy!**
2. Streamlit will take a minute or two to install your packages from `requirements.txt` and boot up your app.
3. Once finished, you will have a public web URL to share with anyone!

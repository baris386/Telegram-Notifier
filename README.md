# 🔔 Telegram Notifier Bot

Telegram Notifier is a modern web application built with **Flask**, **Turso Database (Cloud SQLite)**, and **Vercel Serverless Hosting**. It allows users to schedule notifications that are dispatched directly to a Telegram chat using **cron-job.org** or **Vercel Cron**.

---

## 🌟 Features

- **Turso Cloud SQLite Database**: High-performance, cloud-native distributed SQLite database.
- **WAL Mode Enabled**: Configured with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) for optimal local concurrency.
- **Vercel Serverless**: Lightweight, fast serverless API endpoints.
- **cron-job.org Ready**: Custom endpoint (`/api/cron` / `/cron`) with cache-invalidation headers designed for external cron job triggers.
- **Sample Database Included**: Pre-configured `database.db` included as a reference schema and example database.
- **Local Fallback**: Automatically falls back to local SQLite when Turso environment variables are omitted.

---

## 🛠️ Local Setup

1. **Clone the repository & install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file in the root directory (refer to `.env.example`):
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   # Optional for local SQLite execution:
   TURSO_DATABASE_URL=libsql://your-database-name-your-org.turso.io
   TURSO_AUTH_TOKEN=your_turso_auth_token
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

---

## ☁️ Creating Turso Database from `database.db`

You can import the included `database.db` file directly into Turso CLI when creating your database instance:

```bash
# Create a new Turso database seeded with database.db
turso db create telegram-notifier --from-file database.db

# Retrieve the Database URL
turso db show telegram-notifier --url

# Generate an Authentication Token
turso db tokens create telegram-notifier
```

---

## ⏰ Setting up Cron Job with `cron-job.org`

1. Deploy your app to Vercel (e.g. `https://your-project.vercel.app`).
2. Go to [cron-job.org](https://cron-job.org) and create a free account.
3. Click **Create Cronjob**:
   - **Title**: Telegram Notifier Trigger
   - **URL**: `https://your-project.vercel.app/api/cron` (or `https://your-project.vercel.app/cron`)
   - **Execution Schedule**: Every 1 minute (or your preferred interval)
   - **HTTP Method**: `GET` (or `POST`)
4. Save the Cronjob. `cron-job.org` will now ping your Vercel deployment automatically!

---

## 🚀 Deploying to Vercel

1. **Push your repository to GitHub** (make sure `database.db` is committed).
2. **Import the project into Vercel**.
3. **Set Environment Variables in Vercel**:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `TURSO_DATABASE_URL`
   - `TURSO_AUTH_TOKEN`

---

## 📁 Project Structure

```
.
├── Frontend/           # HTML, CSS, JavaScript frontend assets
├── app.py              # Flask app & Vercel API entrypoint
├── init_db.py          # Database operations (Turso & SQLite WAL mode)
├── scheduler.py        # Telegram notification sender logic
├── database.db         # Pre-configured sample SQLite database file
├── vercel.json         # Vercel deployment configuration
├── requirements.txt    # Production Python dependencies
├── .env.example        # Environment variables template
└── README.md           # Documentation
```

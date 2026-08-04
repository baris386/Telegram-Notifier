<<<<<<< HEAD
# 🔔 Telegram Notifier Bot

Telegram Notifier is a web application built with **Flask**, **Turso Database (Cloud SQLite)**, and **Vercel Serverless Hosting** equipped with **Vercel Cron**. It allows users to schedule notifications that are sent directly to a Telegram chat.

---

## 🌟 Features

- **Turso Cloud SQLite Database**: High-performance distributed SQLite database.
- **WAL Mode Enabled**: Configured with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) for optimal concurrency.
- **Vercel Serverless & Cron**: Serverless deployment with automatic cron invocation (`/api/cron`) every minute.
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

## 🚀 Deploying to Vercel

1. **Push your repository to GitHub** (make sure `database.db` is committed).
2. **Import the project into Vercel**.
3. **Set Environment Variables in Vercel**:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `TURSO_DATABASE_URL`
   - `TURSO_AUTH_TOKEN`

4. **Automatic Cron**:
   - `vercel.json` automatically sets up Vercel Cron to trigger `/api/cron` every minute (`* * * * *`) to check and send due notifications.

---

## 📁 Project Structure

```
.
├── Frontend/           # HTML, CSS, JavaScript frontend assets
├── app.py              # Flask app & Vercel API entrypoint
├── init_db.py          # Database operations (Turso & SQLite WAL mode)
├── scheduler.py        # Telegram notification sender logic
├── database.db         # Pre-configured sample SQLite database file
├── vercel.json         # Vercel deployment & Cron configuration
├── requirements.txt    # Production Python dependencies
├── .env.example        # Environment variables template
└── README.md           # Documentation
```
=======
# 🔔 Telegram Notifier & Alert Dashboard

**Telegram Notifier** is a responsive web application designed to help you manage schedules and stay updated. Set custom tasks with specific dates and times, and receive automated notifications delivered straight to your Telegram chat.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## ✨ Features

* 📅 **Task & Schedule Management:** Easily create notifications with custom titles, messages, dates, and times via an interactive dashboard interface.
* ⚡ **Full CRUD Functionality:** Edit scheduled alerts, delete outdated ones, or track their real-time delivery status (`Pending` / `Sent`).
* 🤖 **Automated Telegram Bot Alerts:** Built-in background worker continually checks active schedules and dispatches instant Telegram messages when triggers expire.
* 🕒 **Timezone Support:** Configured for seamless execution and accurate notification triggers in the Azerbaijan Timezone (UTC+4).

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Task Scheduling:** APScheduler (BackgroundScheduler)
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Deployment:** Render

---

## 🚀 Local Setup Guide

Follow these steps to run the project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
>>>>>>> 4fa81e241f21feb4eb14421698f6cf0de8b4e406

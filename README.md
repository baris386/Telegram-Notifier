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

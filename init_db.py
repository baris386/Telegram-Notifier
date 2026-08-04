import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "").strip()
TURSO_AUTH_TOKEN   = os.environ.get("TURSO_AUTH_TOKEN", "").strip()

def _is_turso():
    return bool(TURSO_DATABASE_URL and TURSO_AUTH_TOKEN)

def _get_turso_client():
    import libsql_client
    url = TURSO_DATABASE_URL
    if url.startswith("libsql://"):
        url = url.replace("libsql://", "https://")
    return libsql_client.create_client_sync(url=url, auth_token=TURSO_AUTH_TOKEN)

def init_db():
    if _is_turso():
        with _get_turso_client() as client:
            client.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    notification_name   TEXT,
                    notification_message TEXT,
                    notification_date   TEXT,
                    notification_time   TEXT,
                    notification_status TEXT
                )
            """)
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_name   TEXT,
                notification_message TEXT,
                notification_date   TEXT,
                notification_time   TEXT,
                notification_status TEXT
            )
        """)
        try:
            cursor.execute("ALTER TABLE notifications ADD COLUMN notification_message TEXT DEFAULT ''")
        except Exception:
            pass
        db.commit()
        db.close()

def add_notification(notification_name, notification_message, notification_date, notification_time, notification_status):
    if _is_turso():
        with _get_turso_client() as client:
            client.execute(
                "INSERT INTO notifications (notification_name, notification_message, notification_date, notification_time, notification_status) VALUES (?, ?, ?, ?, ?)",
                [notification_name, notification_message, notification_date, notification_time, notification_status]
            )
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO notifications (notification_name, notification_message, notification_date, notification_time, notification_status) VALUES (?, ?, ?, ?, ?)",
            (notification_name, notification_message, notification_date, notification_time, notification_status)
        )
        db.commit()
        db.close()

def get_all_notifications():
    if _is_turso():
        with _get_turso_client() as client:
            res = client.execute("SELECT notification_id, notification_name, notification_message, notification_date, notification_time, notification_status FROM notifications")
            return [tuple(row) for row in res.rows]
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT notification_id, notification_name, notification_message, notification_date, notification_time, notification_status FROM notifications")
        rows = cursor.fetchall()
        db.close()
        return rows

def delete_notification(notification_id):
    if _is_turso():
        with _get_turso_client() as client:
            client.execute("DELETE FROM notifications WHERE notification_id = ?", [notification_id])
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("DELETE FROM notifications WHERE notification_id = ?", (notification_id,))
        db.commit()
        db.close()

def update_notification(notification_id, notification_name, notification_message, notification_date, notification_time, notification_status):
    if _is_turso():
        with _get_turso_client() as client:
            client.execute(
                "UPDATE notifications SET notification_name = ?, notification_message = ?, notification_date = ?, notification_time = ?, notification_status = ? WHERE notification_id = ?",
                [notification_name, notification_message, notification_date, notification_time, notification_status, notification_id]
            )
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute(
            "UPDATE notifications SET notification_name = ?, notification_message = ?, notification_date = ?, notification_time = ?, notification_status = ? WHERE notification_id = ?",
            (notification_name, notification_message, notification_date, notification_time, notification_status, notification_id)
        )
        db.commit()
        db.close()

def get_pending_notifications():
    if _is_turso():
        with _get_turso_client() as client:
            res = client.execute(
                "SELECT notification_id, notification_name, notification_message, notification_date, notification_time, notification_status "
                "FROM notifications WHERE notification_status = 'Pending'"
            )
            return [tuple(row) for row in res.rows]
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute(
            "SELECT notification_id, notification_name, notification_message, notification_date, notification_time, notification_status "
            "FROM notifications WHERE notification_status = 'Pending'"
        )
        rows = cursor.fetchall()
        db.close()
        return rows

def mark_as_sent(notification_id):
    if _is_turso():
        with _get_turso_client() as client:
            client.execute(
                "UPDATE notifications SET notification_status = 'Sent' WHERE notification_id = ?",
                [notification_id]
            )
    else:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute(
            "UPDATE notifications SET notification_status = 'Sent' WHERE notification_id = ?",
            (notification_id,)
        )
        db.commit()
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized in WAL mode successfully.")
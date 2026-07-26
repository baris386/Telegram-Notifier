import sqlite3

def init_db():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id     INTEGER PRIMARY KEY,
            notification_name   TEXT,
            notification_message TEXT,
            notification_date   TEXT,
            notification_time   TEXT,
            notification_status TEXT
        )
    """)
    # Köhnə bazada message sütunu yoxdursa əlavə et
    try:
        cursor.execute("ALTER TABLE notifications ADD COLUMN notification_message TEXT DEFAULT ''")
    except Exception:
        pass  # Sütun artıq mövcuddur
    db.commit()
    db.close()

def add_notification(notification_name, notification_message, notification_date, notification_time, notification_status):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO notifications (notification_name, notification_message, notification_date, notification_time, notification_status) VALUES (?, ?, ?, ?, ?)",
        (notification_name, notification_message, notification_date, notification_time, notification_status)
    )
    db.commit()
    db.close()

def get_all_notifications():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT notification_id, notification_name, notification_message, notification_date, notification_time, notification_status FROM notifications")
    rows = cursor.fetchall()
    db.close()
    return rows

def delete_notification(notification_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM notifications WHERE notification_id = ?", (notification_id,))
    db.commit()
    db.close()

def update_notification(notification_id, notification_name, notification_message, notification_date, notification_time, notification_status):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(
        "UPDATE notifications SET notification_name = ?, notification_message = ?, notification_date = ?, notification_time = ?, notification_status = ? WHERE notification_id = ?",
        (notification_name, notification_message, notification_date, notification_time, notification_status, notification_id)
    )
    db.commit()
    db.close()

def get_pending_notifications():
    """Statusu Pending olan bütün bildirişləri qaytarır."""
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
    """Bildirişin statusunu Sent-ə dəyişir."""
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
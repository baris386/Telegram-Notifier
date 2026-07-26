import requests
from datetime import datetime
import init_db as db
import config

def send_telegram_message(text):
    """Telegram Bot API vasitəsilə mesaj göndərir."""
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.ok
    except Exception as e:
        print(f"[Scheduler] Telegram göndərmə xətası: {e}")
        return False


def _parse_scheduled_datetime(notif_date, notif_time):
    raw_time = (notif_time or "").strip()
    if len(raw_time) == 5:
        raw_time = f"{raw_time}:00"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(f"{notif_date} {raw_time}", fmt)
        except ValueError:
            continue
    return None


def check_and_send_notifications():
    """
    Hər bir neçə saniyədə çağırılır.
    Pending bildirişlər arasında vaxtı gəlmiş olanları tapır,
    Telegram-a göndərir, statusu Sent edir.
    """
    now = datetime.now()
    pending = db.get_pending_notifications()

    for notif in pending:
        notif_id      = notif[0]
        notif_name    = notif[1]
        notif_message = notif[2]
        notif_date    = notif[3]
        notif_time    = notif[4]

        scheduled_dt = _parse_scheduled_datetime(notif_date, notif_time)
        if scheduled_dt is None:
            continue

        if now >= scheduled_dt:
            # Mesajı formatla və göndər
            text = (
                f"🔔 <b>{notif_name}</b>\n\n"
                f"{notif_message}\n\n"
                f"📅 {notif_date}  ⏰ {notif_time}"
            )
            success = send_telegram_message(text)

            if success:
                db.mark_as_sent(notif_id)
                print(f"[Scheduler] ✅ Göndərildi → ID={notif_id} | {notif_name}")
            else:
                print(f"[Scheduler] ❌ Göndərilmədi → ID={notif_id} | {notif_name}")

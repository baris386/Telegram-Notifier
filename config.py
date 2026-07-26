import os
from dotenv import load_dotenv

# .env faylı varsa yüklə (local development üçün)
load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")

if not BOT_TOKEN:
    raise EnvironmentError("❌ TELEGRAM_BOT_TOKEN mühit dəyişəni təyin edilməyib!")
if not CHAT_ID:
    raise EnvironmentError("❌ TELEGRAM_CHAT_ID mühit dəyişəni təyin edilməyib!")


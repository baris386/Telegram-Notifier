import init_db as db

# Test məlumatlarını bazaya daxil edirik
db.add_notification("Codeforces Contest Reminder", "Codeforces Round #950 başlayır!", "2026-07-28", "19:35", "Pending")
db.add_notification("Python Bot Deployment Check", "Bot serverini yoxla — uptime ok?", "2026-08-01", "12:00", "Pending")

print("Test məlumatları uğurla bazaya əlavə olundu!")
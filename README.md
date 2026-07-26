# 🔔 Telegram Notifier & Alert Dashboard

**Telegram Notifier**, tapşırıqlarınızı və bildirişlərinizi idarə etmək üçün hazırlanmış veb-əsaslı idarəetmə panelidir. Müəyyən etdiyiniz tarix və saat çatdıqda, sistem avtomatik olaraq Telegram botu vasitəsilə sizə bildiriş göndərir.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## ✨ Özəlliklər

* 📅 **Təqvim və Tapşırıq İdarəetməsi:** Bildirişləri tarix, saat, ad və mesaj daxil edərək asanlıqla yaradın.
* ⚡ **Canlı Yenilənmə (CRUD):** Mövcud bildirişləri redaktə edin (`Edit`), silin (`Delete`) və ya statusunu izləyin.
* 🤖 **Telegram Bot İnteqrasiyası:** Vaxtı gələn tapşırıqlar arxa fonda çalışan scheduler vasitəsilə avtomatik Telegram-a mesaj kimi göndərilir.
* 🕒 **Timezone Dəstəyi:** Bakı saatı (UTC+4) ilə tam uyğunlaşdırılmış bildiriş sistemi.

---

## 🛠️ Texnologiyalar

* **Backend:** Python, Flask
* **Task Scheduler:** APScheduler (BackgroundScheduler)
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Hosting / Deployment:** Render

---

## 🚀 Quraşdırma (Local Setup)

Layihəni öz kompüterinizdə işə salmaq üçün bu addımları izləyin:

1. **Repozitoriyanı klonlayın:**
   ```bash
   git clone [https://github.com/ISTIFADECE_ADI/telegram-notifier.git](https://github.com/ISTIFADECE_ADI/telegram-notifier.git)
   cd telegram-notifier

from flask import jsonify, Flask, render_template, request, redirect, url_for
<<<<<<< HEAD
=======
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
>>>>>>> 4fa81e241f21feb4eb14421698f6cf0de8b4e406
import init_db as db
import scheduler as notif_scheduler

# Serverin saat qurşağını Bakı vaxtına (Asia/Baku) keçiririk
os.environ['TZ'] = 'Asia/Baku'

app = Flask(__name__, template_folder='Frontend', static_folder='Frontend', static_url_path='')

<<<<<<< HEAD
@app.before_request
def ensure_db():
    if not getattr(app, '_db_initialized', False):
        try:
            db.init_db()
            app._db_initialized = True
        except Exception as e:
            print(f"DB Init Error: {e}")
=======
# Server hər dəfə başlayanda cədvəlin varlığını yoxlayır, yoxdursa özü yaradır
with app.app_context():
    db.init_db()

# Scheduler obyektini yaradırıq
_scheduler = BackgroundScheduler()
_scheduler.add_job(
    func=notif_scheduler.check_and_send_notifications,
    trigger='interval',
    seconds=5,
    id='notif_check',
    replace_existing=True,
    next_run_time=datetime.now()
)
>>>>>>> 4fa81e241f21feb4eb14421698f6cf0de8b4e406

# Render / Gunicorn mühitində scheduler-in mütləq işə düşməsini təmin edirik
if not _scheduler.running:
    _scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    notification_name    = request.form['notification_name']
    notification_message = request.form['notification_message']
    notification_date    = request.form['notification_date']
    notification_time    = request.form['notification_time']
    
    db.add_notification(notification_name, notification_message, notification_date, notification_time, 'Pending')
    return redirect(url_for('index'))

@app.route('/edit/<int:notification_id>', methods=['POST'])
def edit(notification_id):
    try:
        notification_name = request.form.get('notification_name')
        notification_message = request.form.get('notification_message')
        notification_date = request.form.get('notification_date')
        notification_time = request.form.get('notification_time')
        notification_status = request.form.get('notification_status')

        db.update_notification(
            notification_id, 
            notification_name, 
            notification_message, 
            notification_date, 
            notification_time, 
            notification_status
        )
        
        return jsonify({"status": "success", "message": "Yeniləndi"}), 200
    except Exception as e:
        print(f"Edit Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete/<int:notification_id>', methods=['POST'])
def delete(notification_id):
    db.delete_notification(notification_id)
    return redirect(url_for('index'))

@app.route('/get_notifications', methods=['GET'])
def get_notifications():
    notifications = db.get_all_notifications()
    notifications_list = []
    for row in notifications:
        notifications_list.append({
            "id":      row[0],
            "name":    row[1],
            "message": row[2],
            "date":    row[3],
            "time":    row[4],
            "status":  row[5]
        })
    return jsonify(notifications_list)

@app.route('/api/cron', methods=['GET', 'POST'])
def cron_trigger():
    """Endpoint executed periodically by Vercel Cron to check and send due notifications."""
    try:
        notif_scheduler.check_and_send_notifications()
        return jsonify({"status": "success", "message": "Cron execution completed"}), 200
    except Exception as e:
        print(f"Cron execution error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
<<<<<<< HEAD
    db.init_db()
    app.run(debug=True)
=======
    app.run(debug=False)
>>>>>>> 4fa81e241f21feb4eb14421698f6cf0de8b4e406

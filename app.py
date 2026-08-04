import os
from flask import jsonify, Flask, render_template, request, redirect, url_for, make_response
import init_db as db
import scheduler as notif_scheduler

# Serverin saat qurşağını Bakı vaxtına (Asia/Baku) keçiririk
os.environ['TZ'] = 'Asia/Baku'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'Frontend')

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path=''
)

@app.before_request
def ensure_db():
    if not getattr(app, '_db_initialized', False):
        try:
            db.init_db()
            app._db_initialized = True
        except Exception as e:
            print(f"DB Init Error: {e}")

@app.route('/')
@app.route('/index')
@app.route('/api/index')
@app.route('/api/index.py')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    try:
        notification_name    = request.form.get('notification_name')
        notification_message = request.form.get('notification_message')
        notification_date    = request.form.get('notification_date')
        notification_time    = request.form.get('notification_time')
        
        if not notification_name or not notification_date or not notification_time:
            return jsonify({"status": "error", "message": "Bütün vacib xanaları doldurun"}), 400

        db.add_notification(notification_name, notification_message or "", notification_date, notification_time, 'Pending')
        
        # Check if request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({"status": "success", "message": "Əlavə olundu"}), 200
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Add Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/edit/<int:notification_id>', methods=['POST'])
def edit(notification_id):
    try:
        notification_name = request.form.get('notification_name')
        notification_message = request.form.get('notification_message')
        notification_date = request.form.get('notification_date')
        notification_time = request.form.get('notification_time')
        notification_status = request.form.get('notification_status')

        db.update_notification(
            int(notification_id), 
            notification_name, 
            notification_message or "", 
            notification_date, 
            notification_time, 
            notification_status or "Pending"
        )
        
        return jsonify({"status": "success", "message": "Yeniləndi"}), 200
    except Exception as e:
        print(f"Edit Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete/<int:notification_id>', methods=['POST'])
def delete(notification_id):
    try:
        db.delete_notification(int(notification_id))
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({"status": "success", "message": "Silindi"}), 200
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Delete Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_notifications', methods=['GET'])
def get_notifications():
    try:
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
    except Exception as e:
        print(f"Get Notifications Error: {e}")
        return jsonify([]), 500

@app.route('/api/cron', methods=['GET', 'POST', 'HEAD'])
@app.route('/cron', methods=['GET', 'POST', 'HEAD'])
def cron_trigger():
    """
    Endpoint executed by cron-job.org (or external ping services / Vercel Cron)
    to check pending notifications and deliver due ones via Telegram.
    """
    try:
        notif_scheduler.check_and_send_notifications()
        res = make_response(jsonify({"status": "success", "message": "Cron job completed successfully"}), 200)
    except Exception as e:
        print(f"Cron execution error: {e}")
        res = make_response(jsonify({"status": "error", "message": str(e)}), 500)
    
    # Disable response caching for cron requests
    res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    res.headers["Pragma"] = "no-cache"
    return res

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)

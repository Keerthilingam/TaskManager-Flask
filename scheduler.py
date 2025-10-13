from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def check_due_tasks():
    from flask import current_app
    with current_app.app_context():
        from models import Task, User
        from email_service import send_due_date_reminder
        
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        
        tasks = Task.query.filter(
            Task.due_date.between(now, tomorrow),
            Task.status != 'completed'
        ).all()
        
        for task in tasks:
            if task.assigned_to:
                user = User.query.get(task.assigned_to)
                if user:
                    send_due_date_reminder(user, task)

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_due_tasks, trigger="interval", hours=24)
    scheduler.start()
    print('Task reminder scheduler initialized')

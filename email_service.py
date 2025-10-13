from flask_mail import Message
from app import mail
from models import Task, User

def send_task_assignment_email(user, task):
    try:
        msg = Message(
            subject=f'New Task Assigned: {task.title}',
            recipients=[user.email],
            body=f'''Hello {user.username},

You have been assigned a new task:

Title: {task.title}
Description: {task.description or 'No description provided'}
Priority: {task.priority.capitalize()}
Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'Not set'}

Please log in to the Task Management System to view and manage this task.

Best regards,
Task Management System
'''
        )
        mail.send(msg)
        print(f'Task assignment email sent to {user.email}')
    except Exception as e:
        print(f'Failed to send email: {e}')

def send_due_date_reminder(user, task):
    try:
        msg = Message(
            subject=f'Task Due Soon: {task.title}',
            recipients=[user.email],
            body=f'''Hello {user.username},

This is a reminder that your task is due soon:

Title: {task.title}
Description: {task.description or 'No description provided'}
Priority: {task.priority.capitalize()}
Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M')}
Status: {task.status.replace('_', ' ').capitalize()}

Please log in to the Task Management System to update this task.

Best regards,
Task Management System
'''
        )
        mail.send(msg)
        print(f'Due date reminder sent to {user.email}')
    except Exception as e:
        print(f'Failed to send email: {e}')

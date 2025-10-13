from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from models import User, Task
from forms import RegistrationForm, LoginForm, TaskForm
from utils import admin_required, manager_required
from datetime import datetime
from sqlalchemy import or_, func

def register_routes(app):
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        status_filter = request.args.get('status', '', type=str)
        priority_filter = request.args.get('priority', '', type=str)
        
        query = Task.query
        
        if not current_user.is_admin():
            query = query.filter(or_(Task.assigned_to == current_user.id, Task.created_by == current_user.id))
        
        if search:
            query = query.filter(or_(Task.title.ilike(f'%{search}%'), Task.description.ilike(f'%{search}%')))
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        if priority_filter:
            query = query.filter_by(priority=priority_filter)
        
        tasks = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
        
        total_tasks = Task.query.filter(or_(Task.assigned_to == current_user.id, Task.created_by == current_user.id)).count() if not current_user.is_admin() else Task.query.count()
        completed_tasks = Task.query.filter_by(status='completed')
        if not current_user.is_admin():
            completed_tasks = completed_tasks.filter(or_(Task.assigned_to == current_user.id, Task.created_by == current_user.id))
        completed_tasks = completed_tasks.count()
        
        pending_tasks = Task.query.filter_by(status='pending')
        if not current_user.is_admin():
            pending_tasks = pending_tasks.filter(or_(Task.assigned_to == current_user.id, Task.created_by == current_user.id))
        pending_tasks = pending_tasks.count()
        
        overdue_tasks = 0
        for task in Task.query.all():
            if not current_user.is_admin() and task.assigned_to != current_user.id and task.created_by != current_user.id:
                continue
            if task.is_overdue():
                overdue_tasks += 1
        
        stats = {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'overdue': overdue_tasks
        }
        
        return render_template('dashboard.html', tasks=tasks, stats=stats, search=search, status_filter=status_filter, priority_filter=priority_filter)

    @app.route('/task/new', methods=['GET', 'POST'])
    @login_required
    def new_task():
        form = TaskForm()
        users = User.query.all()
        form.assigned_to.choices = [(0, 'Unassigned')] + [(u.id, u.username) for u in users]
        
        if form.validate_on_submit():
            assigned_user_id = form.assigned_to.data if form.assigned_to.data != 0 else None
            
            if assigned_user_id and assigned_user_id != current_user.id:
                if not current_user.is_manager():
                    flash('Only managers and admins can assign tasks to other users.', 'danger')
                    return redirect(url_for('dashboard'))
            
            task = Task(
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data,
                status=form.status.data,
                due_date=form.due_date.data,
                created_by=current_user.id,
                assigned_to=assigned_user_id
            )
            db.session.add(task)
            db.session.commit()
            
            if task.assigned_to:
                from email_service import send_task_assignment_email
                assignee = User.query.get(task.assigned_to)
                send_task_assignment_email(assignee, task)
            
            flash('Task created successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('task_form.html', form=form, action='Create')

    @app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_task(task_id):
        task = Task.query.get_or_404(task_id)
        
        if not current_user.is_admin() and task.created_by != current_user.id and task.assigned_to != current_user.id:
            flash('You do not have permission to edit this task.', 'danger')
            return redirect(url_for('dashboard'))
        
        form = TaskForm()
        users = User.query.all()
        form.assigned_to.choices = [(0, 'Unassigned')] + [(u.id, u.username) for u in users]
        
        if form.validate_on_submit():
            old_assignee = task.assigned_to
            new_assignee = form.assigned_to.data if form.assigned_to.data != 0 else None
            
            if new_assignee and new_assignee != current_user.id and new_assignee != old_assignee:
                if not current_user.is_manager():
                    flash('Only managers and admins can reassign tasks to other users.', 'danger')
                    return redirect(url_for('dashboard'))
            
            task.title = form.title.data
            task.description = form.description.data
            task.priority = form.priority.data
            task.status = form.status.data
            task.due_date = form.due_date.data
            task.assigned_to = new_assignee
            db.session.commit()
            
            if task.assigned_to and task.assigned_to != old_assignee:
                from email_service import send_task_assignment_email
                assignee = User.query.get(task.assigned_to)
                send_task_assignment_email(assignee, task)
            
            flash('Task updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        elif request.method == 'GET':
            form.title.data = task.title
            form.description.data = task.description
            form.priority.data = task.priority
            form.status.data = task.status
            form.due_date.data = task.due_date
            form.assigned_to.data = task.assigned_to if task.assigned_to else 0
        
        return render_template('task_form.html', form=form, action='Edit', task=task)

    @app.route('/task/<int:task_id>/delete', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        
        if not current_user.is_admin() and task.created_by != current_user.id:
            flash('You do not have permission to delete this task.', 'danger')
            return redirect(url_for('dashboard'))
        
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('dashboard'))

    @app.route('/analytics')
    @login_required
    @manager_required
    def analytics():
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter_by(status='completed').count()
        pending_tasks = Task.query.filter_by(status='pending').count()
        in_progress_tasks = Task.query.filter_by(status='in_progress').count()
        
        overdue_count = 0
        for task in Task.query.all():
            if task.is_overdue():
                overdue_count += 1
        
        completion_rate = round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
        
        priority_stats = {
            'high': Task.query.filter_by(priority='high').count(),
            'medium': Task.query.filter_by(priority='medium').count(),
            'low': Task.query.filter_by(priority='low').count()
        }
        
        user_stats = []
        users = User.query.all()
        for user in users:
            user_tasks = Task.query.filter_by(assigned_to=user.id).count()
            user_completed = Task.query.filter_by(assigned_to=user.id, status='completed').count()
            user_stats.append({
                'username': user.username,
                'total_tasks': user_tasks,
                'completed_tasks': user_completed,
                'completion_rate': round((user_completed / user_tasks * 100), 2) if user_tasks > 0 else 0
            })
        
        stats = {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'in_progress': in_progress_tasks,
            'overdue': overdue_count,
            'completion_rate': completion_rate,
            'priority': priority_stats,
            'users': user_stats
        }
        
        return render_template('analytics.html', stats=stats)

    @app.route('/users')
    @login_required
    @admin_required
    def users():
        all_users = User.query.all()
        return render_template('users.html', users=all_users)

    @app.route('/user/<int:user_id>/role', methods=['POST'])
    @login_required
    @admin_required
    def change_role(user_id):
        user = User.query.get_or_404(user_id)
        new_role = request.form.get('role')
        
        if new_role in ['user', 'manager', 'admin']:
            user.role = new_role
            db.session.commit()
            flash(f'Role updated for {user.username}!', 'success')
        else:
            flash('Invalid role!', 'danger')
        
        return redirect(url_for('users'))

# Intelligent Task Management System

## Overview
A comprehensive Flask-based task management application featuring user authentication, role-based access control (Admin, Manager, User), CRUD operations for tasks, email notifications, analytics dashboard, and responsive UI with Bootstrap 5.

## Project Status
✅ Fully functional and running on port 5000

## Recent Changes (October 13, 2025)
- Set up Flask application with PostgreSQL database
- Implemented user authentication with Flask-Login and bcrypt password hashing
- Created role-based access control with three user roles (Admin, Manager, User)
- Built complete task CRUD operations with filtering and search
- Integrated email notification system for task assignments and reminders
- Developed analytics dashboard with task metrics and user productivity stats
- Designed responsive UI with Bootstrap 5

## Project Architecture

### Backend Stack
- **Framework**: Flask (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-Login + Flask-Bcrypt
- **Forms**: Flask-WTF with WTForms validation
- **Email**: Flask-Mail for notifications
- **Scheduler**: APScheduler for automated reminders

### Database Models
1. **User Model**
   - Fields: id, username, email, password (hashed), role, created_at
   - Roles: user, manager, admin
   - Relationships: tasks_created, tasks_assigned

2. **Task Model**
   - Fields: id, title, description, priority, status, due_date, created_at, updated_at
   - Foreign Keys: created_by, assigned_to
   - States: pending, in_progress, completed
   - Priorities: low, medium, high

### Application Structure
```
app.py              # Main application entry
config.py           # Configuration
extensions.py       # Flask extensions
models.py           # Database models
routes.py           # Application routes
forms.py            # WTForms definitions
utils.py            # Helper functions
email_service.py    # Email notifications
scheduler.py        # Background tasks
templates/          # Jinja2 templates
static/            # CSS and assets
```

### Key Features
1. **Authentication & Authorization**
   - Secure registration and login
   - Password hashing with bcrypt
   - Session management with Flask-Login
   - Role-based route protection

2. **Task Management**
   - Create, read, update, delete tasks
   - Task assignment to users
   - Search and filter (status, priority, keywords)
   - Overdue task tracking
   - Pagination for task lists

3. **Email Notifications**
   - Task assignment alerts
   - Due date reminders (24-hour check)
   - Configurable SMTP settings

4. **Analytics Dashboard**
   - Task completion rates
   - Priority distribution
   - User productivity metrics
   - Overdue task statistics

5. **User Management (Admin Only)**
   - View all users
   - Change user roles
   - Monitor user activity

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection (auto-configured)
- `SESSION_SECRET`: Flask session key (auto-configured)
- `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`: Email settings (optional)

### Default Credentials
- Admin Email: admin@taskmanager.com
- Admin Password: admin123
- **Important**: Change password after first login

### User Preferences
- Clean, simple dashboard design
- Responsive layout for all devices
- Bootstrap 5 for modern UI components
- Intuitive navigation and user experience

## Next Steps / Future Enhancements
- Real-time notifications with WebSockets
- Task comments and collaboration
- File attachments for tasks
- Advanced analytics with Chart.js/Plotly
- Task templates and recurring tasks
- Export functionality (PDF, CSV)
- Calendar view for tasks
- Task categories and tags

## Technical Notes
- Application runs on port 5.0 (required for Replit)
- Uses PostgreSQL development database
- Email notifications optional (prints to console if not configured)
- Background scheduler runs daily for due date reminders
- CSRF protection enabled on all forms
- LSP warnings are type-checker issues (do not affect runtime)

# Intelligent Task Management System

A comprehensive Flask-based task management application with user authentication, role-based access control, email notifications, and analytics dashboard.

## Features

### Core Functionality
- **User Authentication**: Secure registration and login system with password hashing using bcrypt
- **Role-Based Access Control (RBAC)**: Three user roles (Admin, Manager, User) with different permissions
- **Task Management**: Full CRUD operations for tasks with title, description, priority, status, and due dates
- **Task Assignment**: Assign tasks to users and track task ownership
- **Search & Filtering**: Filter tasks by status, priority, and search by keywords

### Advanced Features
- **Email Notifications**: Automated email alerts for task assignments using Flask-Mail
- **Due Date Reminders**: Scheduled reminders for tasks approaching their due dates
- **Analytics Dashboard**: Comprehensive metrics including:
  - Task completion rates
  - Overdue task tracking
  - Priority distribution
  - User productivity statistics
- **Responsive Design**: Clean, modern UI using Bootstrap 5 that works on all devices

### User Roles & Permissions
- **User**: Can create, edit, and view their own tasks and assigned tasks
- **Manager**: User permissions + access to analytics dashboard
- **Admin**: Full system access including user management and role assignment

## Getting Started

### Default Admin Account
The system creates a default admin account on first run:
- Email: `admin@taskmanager.com`
- Password: `admin123`

**Important**: Change this password after first login for security!

### Installation

1. The application uses PostgreSQL database (already configured)
2. All Python dependencies are installed automatically
3. The Flask app runs on port 5000

### Environment Variables

The following environment variables are available:
- `DATABASE_URL`: PostgreSQL connection string (auto-configured)
- `SESSION_SECRET`: Secret key for Flask sessions (auto-generated)
- `MAIL_SERVER`: SMTP server for email notifications (optional)
- `MAIL_PORT`: SMTP port (default: 587)
- `MAIL_USERNAME`: Email account username (optional)
- `MAIL_PASSWORD`: Email account password (optional)

**Note**: Email notifications are optional. If not configured, the system will print email content to console.

## Usage Guide

### For Users
1. **Register**: Create an account with username, email, and password
2. **Create Tasks**: Add new tasks with priority, status, and due dates
3. **Manage Tasks**: Edit, update status, or delete your tasks
4. **Search**: Use the search and filter options to find specific tasks

### For Managers
- Access all user features
- View the Analytics Dashboard for insights:
  - Overall task completion rates
  - Priority distribution charts
  - User productivity metrics

### For Admins
- Access all manager features
- **User Management**: View all users and change their roles
- **Full Task Access**: View and manage all tasks in the system

## Task Features

### Task Properties
- **Title**: Brief description of the task
- **Description**: Detailed task information
- **Priority**: Low, Medium, or High
- **Status**: Pending, In Progress, or Completed
- **Due Date**: Optional deadline with time
- **Assignment**: Assign to specific users

### Task States
- **Pending**: Newly created tasks
- **In Progress**: Tasks currently being worked on
- **Completed**: Finished tasks
- **Overdue**: Tasks past their due date (highlighted in red)

## Email Notifications

The system sends automated emails for:
1. **Task Assignment**: When a task is assigned to a user
2. **Due Date Reminders**: Daily check for tasks due within 24 hours

To enable email notifications, configure these environment variables:
- `MAIL_SERVER`: Your SMTP server (e.g., smtp.gmail.com)
- `MAIL_USERNAME`: Your email address
- `MAIL_PASSWORD`: Your email password or app-specific password

## Analytics Dashboard

Managers and Admins can access detailed analytics:
- **Task Overview**: Total, completed, pending, and overdue tasks
- **Completion Rate**: Percentage of completed tasks
- **Priority Distribution**: Visual breakdown of task priorities
- **User Productivity**: Individual user performance metrics

## Security Features

- **Password Hashing**: All passwords encrypted with bcrypt
- **Session Management**: Secure user sessions with Flask-Login
- **CSRF Protection**: Form protection with Flask-WTF
- **Role-Based Access**: Route protection based on user roles
- **Input Validation**: Server-side validation for all forms

## Project Structure

```
├── app.py                 # Main application entry point
├── config.py             # Configuration settings
├── extensions.py         # Flask extensions initialization
├── models.py             # Database models (User, Task)
├── routes.py             # Application routes and views
├── forms.py              # WTForms form definitions
├── utils.py              # Utility functions and decorators
├── email_service.py      # Email notification functions
├── scheduler.py          # Background task scheduler
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── task_form.html
│   ├── analytics.html
│   └── users.html
└── static/               # Static files (CSS, JS)
    └── css/
        └── style.css
```

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-Login with Bcrypt
- **Forms**: Flask-WTF with WTForms
- **Email**: Flask-Mail
- **Scheduler**: APScheduler
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Template Engine**: Jinja2

## Future Enhancements

Potential features for future releases:
- Real-time notifications using WebSockets
- Task comments and collaboration
- File attachments for tasks
- Advanced analytics with charts (Chart.js/Plotly)
- Task templates and recurring tasks
- Export functionality (PDF, CSV)
- Task categories and tags
- Calendar view for tasks

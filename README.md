# Intelligent Task Management System

A comprehensive Flask-based task management application with user authentication, role-based access control, email notifications, and analytics dashboard.

## Features

- 🔐 **User Authentication**: Secure registration and login with password hashing (bcrypt)
- 👥 **Role-Based Access Control**: Three user roles (Admin, Manager, User)
- ✅ **Task Management**: Full CRUD operations with priority, status, and due dates
- 📧 **Email Notifications**: Automated alerts for task assignments
- ⏰ **Due Date Reminders**: Scheduled notifications for upcoming deadlines
- 📊 **Analytics Dashboard**: Task completion rates, priority distribution, user productivity
- 🔍 **Search & Filter**: Find tasks by status, priority, or keywords
- 📱 **Responsive Design**: Bootstrap 5 UI that works on all devices

## Default Admin Account

The system creates a default admin account on first run:
- **Email**: `admin@taskmanager.com`
- **Password**: `admin123`

⚠️ **Important**: Change this password immediately after first login!

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher

### Step 1: Install PostgreSQL

**Windows:**
1. Download from [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
2. Run installer and follow setup wizard
3. Remember the password you set for `postgres` user
4. Default port: 5432

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### Step 2: Create Database

Open PostgreSQL command line (psql):

**Windows:** Search "SQL Shell (psql)" in Start Menu

**Linux/Mac:**
```bash
sudo -u postgres psql
```

Then create database:
```sql
CREATE DATABASE taskmanager;
CREATE USER taskuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskuser;
\q
```

### Step 3: Clone Repository

```bash
git clone https://github.com/Keerthilingam/TaskManager-Flask.git
cd TaskManager-Flask
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Create `requirements.txt` if not exists:
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==3.0.1
Flask-Mail==0.9.1
APScheduler==3.10.1
bcrypt==4.0.1
email-validator==2.0.0
psycopg2-binary==2.9.6
WTForms==3.0.1
```

### Step 5: Configure Environment Variables

Create a `.env` file in project root:

```env
# Database Configuration
DATABASE_URL=postgresql://taskuser:your_password@localhost:5432/taskmanager

# Flask Configuration
SESSION_SECRET=your-secret-key-here-change-this
FLASK_ENV=development

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Database URL Format:**
```
postgresql://username:password@host:port/database_name
```

**Example:**
```
postgresql://taskuser:mypass123@localhost:5432/taskmanager
```

### Step 6: Initialize Database

```bash
python app.py
```

On first run, the application will:
- Create all database tables automatically
- Create default admin account
- Start the Flask server on `http://localhost:5000`

### Step 7: Access Application

Open your browser and go to: `http://localhost:5000`

Login with admin credentials and start using!

## Configuration Details

### Database Connection Explained

**Format:** `postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE`

- **USERNAME**: PostgreSQL user (e.g., `taskuser`)
- **PASSWORD**: User's password (e.g., `mypass123`)
- **HOST**: Database server (usually `localhost`)
- **PORT**: PostgreSQL port (default: `5432`)
- **DATABASE**: Database name (e.g., `taskmanager`)

### Email Setup (Optional)

For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Use App Password in `MAIL_PASSWORD`

**Note:** If email is not configured, notifications will print to console.

## User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **User** | Create, edit, delete own tasks; View assigned tasks |
| **Manager** | All User permissions + Analytics dashboard access |
| **Admin** | All Manager permissions + User management + View all tasks |

## Usage Guide

### For Regular Users
1. **Register**: Create account with username, email, password
2. **Create Tasks**: Click "New Task" and fill details
3. **Manage Tasks**: Edit status, priority, or delete tasks
4. **Search**: Use filters to find specific tasks

### For Managers
- Access Analytics Dashboard for insights
- View team productivity metrics
- Track task completion rates

### For Admins
- Manage user roles (User → Manager → Admin)
- View and manage all system tasks
- Access complete analytics

## Project Structure

```
TaskManager-Flask/
├── app.py              # Main application entry
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions
├── models.py           # Database models (User, Task)
├── routes.py           # Application routes
├── forms.py            # WTForms definitions
├── utils.py            # Utility functions
├── email_service.py    # Email notifications
├── scheduler.py        # Background scheduler
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── task_form.html
│   ├── analytics.html
│   └── users.html
└── static/
    └── css/
        └── style.css
```

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** Flask-Login, Bcrypt
- **Forms:** Flask-WTF, WTForms
- **Email:** Flask-Mail
- **Scheduler:** APScheduler
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Template Engine:** Jinja2

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
**Solution:** Check if PostgreSQL service is running:
```bash
# Windows
services.msc -> PostgreSQL

# Linux
sudo systemctl status postgresql

# Mac
brew services list
```

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001)
```

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Install requirements again:
```bash
pip install -r requirements.txt
```

## Security Features

- Password hashing with bcrypt
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Role-based route protection
- SQL injection prevention with SQLAlchemy ORM

## Future Enhancements

- Real-time notifications (WebSockets)
- Task comments and collaboration
- File attachments
- Advanced charts (Chart.js/Plotly)
- Task templates and recurring tasks
- Export to PDF/CSV
- Calendar view
- Task categories and tags

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
- Create an issue on GitHub
- Contact: [Your Email]

---

**Made with ❤️ using Flask and PostgreSQL**

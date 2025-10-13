from flask import Flask
from config import Config
from extensions import db, bcrypt, mail, login_manager
from models import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from utils import create_default_admin
        create_default_admin()
        from scheduler import init_scheduler
        init_scheduler()
    app.run(host='0.0.0.0', port=5000, debug=True)

# app/create_app.py

from flask import Flask
from flask_migrate import Migrate

from .config import Config, ConfigDebug, ConfigTesting
from .models import db, User
from .auth.views import auth_bp
from .main.views import main_bp
from flask_login import LoginManager, current_user
from datetime import datetime


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate = Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

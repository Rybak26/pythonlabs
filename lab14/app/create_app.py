# app/create_app.py

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config, ConfigDebug, ConfigTesting
from .models import db, User, Todo
from .auth.views import auth_bp
from .main.views import main_bp
from .todo.views import todos_bp
from .todo.api_todo import api_todo_bp
from .post.views import posts_bp
from flask_login import LoginManager, current_user
from datetime import datetime, timezone

jwt = JWTManager()


def create_app(config_class=ConfigDebug):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate = Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    jwt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now(timezone.utc)
            db.session.commit()

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(todos_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(api_todo_bp)

    return app

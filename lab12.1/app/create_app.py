
from flask import Flask
from flask_migrate import Migrate
from app.config import Config, ConfigDebug, ConfigTesting
from app.models import db, User, Todo
from app.auth.views import auth_bp
from app.main.views import main_bp
from app.todo.views import todos_bp
from app.post.views import posts_bp
from flask_login import LoginManager, current_user
from datetime import datetime


def create_app(config_class=ConfigDebug):
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
    app.register_blueprint(todos_bp)
    app.register_blueprint(posts_bp)

    return app

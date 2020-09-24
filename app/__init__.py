from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)

    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    from app.authentication import user_bp
    app.register_blueprint(user_bp)

    return app

from app import models

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrilog.db'
    db.init_app(app)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    from .pages import pages
    from .auth import auth

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.register_blueprint(pages, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .database import User, Food

    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists('instance/nutrilog.db'):
        with app.app_context():
            db.create_all()

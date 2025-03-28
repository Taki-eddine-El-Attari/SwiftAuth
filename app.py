from flask import Flask, redirect, url_for
from flask_session import Session
from config import Config
from models.user import db, User
from views.auth_views import auth_bp
from utils.cache import init_cache
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    Session(app)
    init_cache(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='')
    
    # Create a route for the root URL
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()


# Application structural imports
from flask import Flask, render_template
from flask_login import LoginManager
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .extensions import db, jwt
from .auth.routes import auth_bp

# Application Specific Imports
from .inventory.routes import inventory_bp
from .recipes.routes import recipes_bp
from .reports.routes import reports_bp
from .grocery_list.routes import grocery_bp
from .models import User

# redirect if not logged in
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 👇 Add this
    from jinja2 import ChoiceLoader, FileSystemLoader
    import os
    app.jinja_loader = ChoiceLoader([
        app.jinja_loader,
        FileSystemLoader(os.path.join(os.path.dirname(__file__), 'auth/templates'))
    ])
    
    jwt.init_app(app)
    # Login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize Database
    db.init_app(app)
    #development database
    with app.app_context():
        from SmartGroceryApp import models
        db.create_all()

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(grocery_bp)

    # Set the application root
    @app.route('/')
    def index():
        return render_template('auth/login.html')
    
    return app

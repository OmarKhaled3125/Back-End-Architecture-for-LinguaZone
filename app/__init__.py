from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os
import logging
from config import Config  # Import your Config class here


# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        # Load from Config class instead of hardcoded dict
        app.config.from_object(Config)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure upload directories exist
    upload_base = os.path.join(app.root_path, 'static', 'uploads')
    for folder in ['levels', 'sections', 'questions']:
        upload_path = os.path.join(upload_base, folder)
        try:
            os.makedirs(upload_path, exist_ok=True)
        except OSError:
            pass

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Register blueprints
    from app.controllers.api.auth_controller import auth_bp
    from app.controllers.api.level_controller import level_bp
    from app.controllers.api.section_controller import section_bp
    from app.controllers.api.question_controller import question_bp
    from app.controllers.api.general_controller import general_bp


    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(level_bp, url_prefix='/api/level')
    app.register_blueprint(section_bp, url_prefix='/api/section')
    app.register_blueprint(question_bp, url_prefix='/api/question')
    app.register_blueprint(general_bp, url_prefix='/api/general')

    with app.app_context():
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)
    
    return app

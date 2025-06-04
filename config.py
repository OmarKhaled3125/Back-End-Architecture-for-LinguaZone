import os
from datetime import timedelta

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:3125@127.0.0.1/language_learning'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    
    # Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'linguazone3125@gmail.com'
    MAIL_PASSWORD = 'fcuojtyzjwrcpltg'
    MAIL_DEFAULT_SENDER = 'linguazone3125@gmail.com'

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size

    
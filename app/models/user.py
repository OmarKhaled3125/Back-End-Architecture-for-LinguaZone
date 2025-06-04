from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    verification_code_expires = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role.value,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

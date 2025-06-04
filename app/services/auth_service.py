from app import db
from app.models.user import User
from app.utils.email import send_verification_email, send_password_reset_email
from app.utils.helpers import generate_verification_code
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

class AuthService:
    @staticmethod
    def register(email, password, username , role):
        """
        Register a new user and return access token
        """
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")

        user = User(
            email=email,
            username=username,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role.value
            }
        }

    @staticmethod
    def verify_email(email, verification_code):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('User not found')
            
        if user.is_verified:
            return {'message': 'Email already verified'}
            
        if not user.verification_code or not user.verification_code_expires:
            raise ValueError('No verification code found')
            
        if datetime.utcnow() > user.verification_code_expires:
            raise ValueError('Verification code has expired')
            
        if user.verification_code != verification_code:
            raise ValueError('Invalid verification code')
        
        user.is_verified = True
        user.verification_code = None
        user.verification_code_expires = None
        db.session.commit()
        
        return {'message': 'Email verified successfully'}

    @staticmethod
    def resend_otp(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('User not found')
            
        if user.is_verified:
            return {'message': 'Email already verified'}
        
        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.verification_code_expires = datetime.utcnow() + timedelta(minutes=30)
        
        if not send_verification_email(user.email, verification_code):
            raise RuntimeError('Failed to send verification email')
            
        db.session.commit()
        return {'message': 'New verification code sent successfully'}

    @staticmethod
    def check_user_email(email):
        user = User.query.filter_by(email=email).first()
        return {
            'exists': bool(user),
            'is_verified': bool(user and user.is_verified) if user else None
        }

    @staticmethod
    def login(email, password):
        """
        Authenticate a user and return a JWT token
        """
        user = User.query.filter_by(email=email, is_verified=True).first()
        
        if not user or not user.check_password(password):
            raise ValueError("Invalid email or password")

        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role.value
            }
        }

    @staticmethod
    def delete_user(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('User not found')
            
        db.session.delete(user)
        db.session.commit()
        
        return {
            'deleted_user': {
                'email': user.email,
                'username': user.username
            }
        }

    @staticmethod
    def forgot_password(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('User not found')
        
        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.verification_code_expires = datetime.utcnow() + timedelta(minutes=30)
        
        if not send_password_reset_email(user.email, verification_code):
            raise RuntimeError('Failed to send verification email')

        db.session.commit()
        return {'message': 'Verification code sent to your email'}

    @staticmethod
    def reset_password(email, verification_code, new_password):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('User not found')
        
        if datetime.utcnow() > user.verification_code_expires:
            raise ValueError('Verification code has expired')
        
        if user.verification_code != verification_code:
            raise ValueError('Invalid verification code')
        
        user.set_password(new_password)
        user.verification_code = None
        user.verification_code_expires = None
        db.session.commit()
        
        return {'message': 'Password updated successfully'} 
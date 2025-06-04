from app.extensions import mail
from flask_mail import Mail, Message
from flask import current_app
import random

def send_verification_email(user_email, verification_code):
    print(f"Preparing to send email to: {user_email} with code: {verification_code}")
    try:
        msg = Message(
            'Verify Your Email - LinguaZone',
            recipients=[user_email]
        )
        msg.html = f'''
        <h2>Welcome to LinguaZone!</h2>
        <p>Thank you for registering. To verify your email address, please use the following verification code:</p>
        <h1 style="color: #4CAF50; font-size: 40px;">{verification_code}</h1>
        <p>This code will expire in 30 minutes.</p>
        <p>If you didn't request this verification, please ignore this email.</p>
        <br>
        <p>Best regards,</p>
        <p>LinguaZone Team</p>
        '''
        print("Message created, attempting to send...")
        mail.send(msg)
        print("Email sent successfully!")
        return True
    except Exception as e:
        import traceback
        print(f"\nDetailed error sending email:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return False

#----------------------------------------------------------------------------

def send_password_reset_email(user_email, verification_code):
    print(f"Preparing to send password reset email to: {user_email} with code: {verification_code}")
    try:
        msg = Message(
            'Reset Your Password - LinguaZone',
            recipients=[user_email]
        )
        msg.html = f'''
        <h2>Password Reset Request</h2>
        <p>We received a request to reset your password. Please use the following verification code:</p>
        <h1 style="color: #4CAF50; font-size: 40px;">{verification_code}</h1>
        <p>This code will expire in 30 minutes.</p>
        <p>If you did not request a password reset, please ignore this email.</p>
        <br>
        <p>Best regards,</p>
        <p>LinguaZone Team</p>
        '''
        print("Message created, attempting to send...")
        mail.send(msg)
        print("Password reset email sent successfully!")
        return True
    except Exception as e:
        import traceback
        print(f"\nDetailed error sending password reset email:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return False
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

#-------------------------------------------------------------

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['email', 'password', 'username' , 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = AuthService.register(
            email=data['email'],
            password=data['password'],
            username=data['username'],
            role=data['role']
        )
        return jsonify({
            'message': 'User registered successfully',
            **result
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('verification_code'):
        return jsonify({'error': 'Email and verification code are required'}), 400
    
    try:
        result = AuthService.verify_email(
            email=data['email'],
            verification_code=data['verification_code']
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    try:
        result = AuthService.resend_otp(email=data['email'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/is-user-email-found', methods=['POST'])
def is_user_email_found():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    result = AuthService.check_user_email(email=data['email'])
    return jsonify(result), 200

#-------------------------------------------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    try:
        result = AuthService.login(
            email=data['email'],
            password=data['password']
        )
        access_token = create_access_token(identity=result['user']['id'])
        refresh_token = create_refresh_token(identity=result['user']['id'])
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            **result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/delete-user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    try:
        result = AuthService.delete_user(email=data['email'])
        return jsonify({'message': 'User deleted successfully', **result}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    try:
        result = AuthService.forgot_password(email=data['email'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/retrieve-password', methods=['POST'])
def retrieve_password():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('verification_code') or not data.get('new_password'):
        return jsonify({'error': 'Email, verification code, and new password are required'}), 400
    
    try:
        result = AuthService.reset_password(
            email=data['email'],
            verification_code=data['verification_code'],
            new_password=data['new_password']
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------------------------

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
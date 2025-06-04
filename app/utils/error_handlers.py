from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow.exceptions import ValidationError
from flask_jwt_extended.exceptions import JWTExtendedException
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

class ResourceNotFoundError(APIError):
    """Exception for when a requested resource is not found"""
    def __init__(self, message="Resource not found", payload=None):
        super().__init__(message, status_code=404, payload=payload)

class AuthenticationError(APIError):
    """Exception for authentication failures"""
    def __init__(self, message="Authentication failed", payload=None):
        super().__init__(message, status_code=401, payload=payload)

class AuthorizationError(APIError):
    """Exception for authorization failures"""
    def __init__(self, message="Not authorized to perform this action", payload=None):
        super().__init__(message, status_code=403, payload=payload)

class ValidationError(APIError):
    """Exception for validation errors"""
    def __init__(self, message="Validation error", payload=None):
        super().__init__(message, status_code=400, payload=payload)

def register_error_handlers(app):
    """Register all error handlers with the Flask app"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle Werkzeug HTTP exceptions"""
        response = jsonify({
            'status': 'error',
            'message': error.description,
            'code': error.code
        })
        response.status_code = error.code
        return response

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        """Handle database errors"""
        logger.error(f"Database error: {str(error)}")
        if isinstance(error, IntegrityError):
            return jsonify({
                'status': 'error',
                'message': 'Database integrity error',
                'details': str(error.orig)
            }), 400
        return jsonify({
            'status': 'error',
            'message': 'Database error occurred'
        }), 500

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle validation errors"""
        return jsonify({
            'status': 'error',
            'message': 'Validation error',
            'details': error.messages
        }), 400

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(error):
        """Handle JWT errors"""
        return jsonify({
            'status': 'error',
            'message': 'Authentication error',
            'details': str(error)
        }), 401

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle all other errors"""
        logger.error(f"Unhandled error: {str(error)}")
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }), 500 
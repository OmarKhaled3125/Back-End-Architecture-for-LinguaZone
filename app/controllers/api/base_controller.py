from typing import Any, Dict, Optional, Tuple
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from app.utils.error_handlers import (
    APIError, ResourceNotFoundError, ValidationError,
    AuthenticationError, AuthorizationError
)


class BaseController:
    
    def __init__(self, name: str, import_name: str, url_prefix: Optional[str] = None):
     
        self.blueprint = Blueprint(name, import_name, url_prefix=url_prefix)
        self._register_error_handlers()
    
    def _register_error_handlers(self) -> None:
        """Register common error handlers for the blueprint."""
        @self.blueprint.errorhandler(HTTPException)
        def handle_http_error(error: HTTPException) -> Tuple[Dict[str, Any], int]:
            """Handle HTTP exceptions."""
            response = {
                'error': error.name,
                'message': error.description,
                'status_code': error.code
            }
            return jsonify(response), error.code
    
    def success_response(self, data: Any = None, message: str = "Success", status_code: int = 200) -> Tuple[Dict[str, Any], int]:
       
        response = {
            'status': 'success',
            'message': message,
            'data': data
        }
        return jsonify(response), status_code
    
    def error_response(self, message: str, status_code: int = 400, errors: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], int]:
        response = {
            'status': 'error',
            'message': message
        }
        if errors:
            response['errors'] = errors
        return jsonify(response), status_code
    
    def get_request_data(self) -> Dict[str, Any]:
        """Get and validate request data."""
        if not request.is_json:
            raise ValidationError("Request must be JSON")
        return request.get_json()
    
    def not_found(self, message: str = "Resource not found") -> None:
        """Raise a not found error."""
        raise ResourceNotFoundError(message)
    
    def validation_error(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None) -> None:
        """Raise a validation error."""
        raise ValidationError(message, payload={'details': details})
    
    def authentication_error(self, message: str = "Authentication failed") -> None:
        """Raise an authentication error."""
        raise AuthenticationError(message)
    
    def authorization_error(self, message: str = "Not authorized") -> None:
        """Raise an authorization error."""
        raise AuthorizationError(message) 
from typing import Dict, Any, Tuple
from flask import request
from werkzeug.exceptions import BadRequest
from app.controllers.api.base_controller import BaseController
from app.services.section_service import SectionService
from app.utils.file_upload import validate_file_upload
from app.utils.auth_decorators import token_required, admin_required


class SectionController(BaseController):
    """Controller for handling section-related operations."""
    
    def __init__(self):
        """Initialize the section controller."""
        super().__init__('section', __name__)
        self.service = SectionService()
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all routes for the section controller."""
        # Register routes with strict_slashes=False to handle both with and without trailing slash
        self.blueprint.route('', methods=['GET'], strict_slashes=False)(token_required(self.get_sections))
        self.blueprint.route('/<int:section_id>', methods=['GET'], strict_slashes=False)(token_required(self.get_section))
        self.blueprint.route('', methods=['POST'], strict_slashes=False)(admin_required(self.create_section))
        self.blueprint.route('/<int:section_id>', methods=['PUT'], strict_slashes=False)(admin_required(self.update_section))
        self.blueprint.route('/<int:section_id>', methods=['DELETE'], strict_slashes=False)(admin_required(self.delete_section))
    
    def get_sections(self) -> Tuple[Dict[str, Any], int]:
        """ Get all sections or filter by level. """
        level_id = request.args.get('level_id', type=int)
        sections = self.service.get_sections_by_level(level_id) if level_id else self.service.get_all()
        return self.success_response(data=[section.to_dict() for section in sections])
    
    def get_section(self, section_id: int) -> Tuple[Dict[str, Any], int]:
        """ Get a specific section by ID. """
        section = self.service.get_by_id(section_id)
        if not section:
            return self.error_response("Section not found", status_code=404)
        return self.success_response(data=section.to_dict())
    
    def create_section(self) -> Tuple[Dict[str, Any], int]:
        """ Create a new section. """
        try:
            # Support both JSON and form-data
            if request.is_json:
                data = request.get_json()
                file = None
            else:
                data = request.form.to_dict()
                file = request.files.get('image')

            if file:
                validate_file_upload(file)

            section = self.service.create_section(data, file)
            section_data = section.to_dict() if hasattr(section, 'to_dict') else section
            return self.success_response(
                data=section_data,
                message="Section created successfully",
                status_code=201
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            return self.error_response("Failed to create section", status_code=500)
    
    def update_section(self, section_id: int) -> Tuple[Dict[str, Any], int]:
        """ Update an existing section. """
        try:
            # Support both JSON and form-data
            if request.is_json:
                data = request.get_json()
                file = None
            else:
                data = request.form.to_dict()
                file = request.files.get('image')

            if file:
                validate_file_upload(file)

            section = self.service.update_section(section_id, data, file)
            if not section:
                return self.error_response("Section not found", status_code=404)
            
            return self.success_response(
                data=section.to_dict(),
                message="Section updated successfully"
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            return self.error_response("Failed to update section", status_code=500)
    
    def delete_section(self, section_id: int) -> Tuple[Dict[str, Any], int]:
        """ Delete a section. """
        try:
            if self.service.delete_section(section_id):
                return self.success_response(message="Section deleted successfully")
            return self.error_response("Section not found", status_code=404)
        except Exception as e:
            return self.error_response("Failed to delete section", status_code=500)


# Create blueprint instance
section_bp = SectionController().blueprint

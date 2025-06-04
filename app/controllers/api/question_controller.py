from typing import Dict, Any, Tuple, Optional
from flask import request
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import FileStorage

from app.controllers.api.base_controller import BaseController
from app.services.question_service import QuestionService
from app.utils.file_upload import validate_file_upload
from app.utils.auth_decorators import token_required, admin_required

import json # Import json for potential parsing in add_choices

class QuestionController(BaseController):
    """Controller for handling question-related operations."""
    
    def __init__(self):
        """Initialize the question controller."""
        super().__init__('question', __name__)
        self.service = QuestionService()
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all routes for the question controller."""
        # Register routes with strict_slashes=False to handle both with and without trailing slash
        self.blueprint.route('', methods=['GET'], strict_slashes=False)(token_required(self.get_questions))
        self.blueprint.route('/<int:question_id>', methods=['GET'], strict_slashes=False)(token_required(self.get_question))
        self.blueprint.route('', methods=['POST'], strict_slashes=False)(admin_required(self.create_question))
        
        # Correctly referencing the method within the class
        self.blueprint.route('/<int:question_id>', methods=['PUT'], strict_slashes=False)(admin_required(self.update_question))
        
        self.blueprint.route('/<int:question_id>', methods=['DELETE'], strict_slashes=False)(admin_required(self.delete_question))
        self.blueprint.route('/<int:question_id>/choices', methods=['POST'], strict_slashes=False)(admin_required(self.add_choices))
        self.blueprint.route('/<int:question_id>/choices/<int:choice_id>', methods=['DELETE'], strict_slashes=False)(admin_required(self.delete_choice))
        self.blueprint.route('/<int:question_id>/choices/<int:choice_id>', methods=['PUT'], strict_slashes=False)(admin_required(self.update_choice))
    
    def get_questions(self) -> Tuple[Dict[str, Any], int]:
        """ Get all questions or filter by section. """
        section_id = request.args.get('section_id', type=int)
        questions = self.service.get_questions_by_section(section_id) if section_id else self.service.get_all()
        return self.success_response(data=[question.to_dict() for question in questions])
    
    def get_question(self, question_id: int) -> Tuple[Dict[str, Any], int]:
        """ Get a specific question by ID. """
        question = self.service.get_by_id(question_id)
        if not question:
            return self.error_response("Question not found", status_code=404)
        return self.success_response(data=question.to_dict())
    
    def create_question(self) -> Tuple[Dict[str, Any], int]:
        """ Create a new question. """
        try:
            data = {}
            question_file = None
            files_for_choices = None

            if request.is_json:
                data = request.get_json()
                # For JSON, 'choices' if present, would already be a list/dict.
                # No files for choices expected directly in request.files for JSON.
            else: # Handle multipart/form-data
                data = request.form.to_dict() # Get form fields as a dict
                question_file = request.files.get('question_content') # Main question media
                files_for_choices = request.files # All files in the request, for choice media

            if question_file:
                validate_file_upload(question_file)

            # Pass files_for_choices to the service method
            question = self.service.create_question(data, question_file, files=files_for_choices)
            return self.success_response(
                data=question.to_dict(),
                message="Question created successfully",
                status_code=201
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error creating question: {e}") 
            return self.error_response("Failed to create question", status_code=500)
    
    def update_question(self, question_id: int) -> Tuple[Dict[str, Any], int]:
        """ Update an existing question."""
        try:
            data = {}
            question_file = None
            files_for_choices = None

            if request.is_json:
                data = request.get_json()
                # For JSON, 'choices' if present, would already be a list/dict.
                # No files for choices expected directly in request.files for JSON.
            else: # Handle multipart/form-data
                data = request.form.to_dict() # Get form fields as a dict
                # Assuming your main question media file input is named 'question_content'
                question_file = request.files.get('question_content') 
                files_for_choices = request.files # All files in the request, for choice media

            if question_file:
                validate_file_upload(question_file)

            # Pass files_for_choices to the service method
            question = self.service.update_question(question_id, data, question_file, files=files_for_choices)
            if not question:
                return self.error_response("Question not found", status_code=404)
            
            return self.success_response(
                data=question.to_dict(),
                message="Question updated successfully"
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error updating question: {e}") 
            return self.error_response("Failed to update question", status_code=500)
    
    def delete_question(self, question_id: int) -> Tuple[Dict[str, Any], int]:
        """ Delete a question. """
        try:
            if self.service.delete_question(question_id):
                return self.success_response(message="Question deleted successfully")
            return self.error_response("Question not found", status_code=404)
        except Exception as e:
            print(f"Error deleting question: {e}") 
            return self.error_response("Failed to delete question", status_code=500)

    def add_choices(self, question_id: int) -> Tuple[Dict[str, Any], int]:
        """
        Add choices to a question. This method expects a list of choices.
        If a single choice is sent, it should still be wrapped in a list.
        """
        try:
            data = {}
            files_for_choices = None

            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
                files_for_choices = request.files
            
            choices_to_add = data.get('choices')
            if not choices_to_add:
                # If 'choices' key is not present, or empty, check if a single choice was sent directly
                # This makes the endpoint more flexible, but ideally, frontend should send a list.
                if 'content' in data and 'choice_type' in data: # Check for keys of a single choice
                    choices_to_add = [data] # Wrap single choice in a list
                else:
                    raise BadRequest("No choices provided in the request.")

            if isinstance(choices_to_add, str):
                try:
                    choices_to_add = json.loads(choices_to_add)
                except json.JSONDecodeError:
                    raise BadRequest("Invalid JSON format for choices.")
            
            if not isinstance(choices_to_add, list):
                raise BadRequest("Choices must be a list of choice objects.")

            # Call a service method that can handle adding multiple choices
            added_choices = self.service.add_multiple_choices(question_id, choices_to_add, files=files_for_choices)
            
            return self.success_response(data=[choice.to_dict() for choice in added_choices], message="Choices added successfully")

        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error adding choice(s): {e}") 
            return self.error_response("Failed to add choice(s)", status_code=500)


    def delete_choice(self, question_id: int, choice_id: int) -> Tuple[Dict[str, Any], int]:
        """
        Delete a specific choice from a question.
        """
        try:
            # The service method handles the choice not found case.
            self.service.delete_choice(question_id, choice_id)
            return self.success_response(message="Choice deleted successfully")
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error deleting choice: {e}") 
            return self.error_response("Failed to delete choice", status_code=500)

    def update_choice(self, question_id: int, choice_id: int) -> Tuple[Dict[str, Any], int]:
        """
        Update a specific choice for a question.
        """
        try:
            data = {}
            files_for_choice = None

            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
                files_for_choice = request.files # Pass all files from request.files

            choice = self.service.update_single_choice(question_id, choice_id, data, files=files_for_choice)
            return self.success_response(data=choice.to_dict(), message="Choice updated successfully")
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error updating choice: {e}") 
            return self.error_response("Failed to update choice", status_code=500)


# Create blueprint instance
question_bp = QuestionController().blueprint
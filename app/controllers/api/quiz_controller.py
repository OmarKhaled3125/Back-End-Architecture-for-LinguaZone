# app/controllers/api/quiz_controller.py

from typing import Dict, Any, Tuple, List, Optional
from flask import request
from werkzeug.exceptions import BadRequest

from app.controllers.api.base_controller import BaseController
from app.services.quiz_service import QuizService # Import your QuizService
from app.utils.auth_decorators import token_required, admin_required

class QuizController(BaseController):
    """Controller for handling quiz-related operations."""
    
    def __init__(self):
        """Initialize the quiz controller."""
        super().__init__('quiz', __name__)
        self.service = QuizService() # Instantiate your QuizService
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all routes for the quiz controller."""
        # Get all quizzes
        self.blueprint.route('', methods=['GET'], strict_slashes=False)(token_required(self.get_all_quizzes))
        
        # Get quiz by ID
        self.blueprint.route('/<int:quiz_id>', methods=['GET'], strict_slashes=False)(token_required(self.get_quiz))
        
        # Get quiz by level ID (unique per level)
        self.blueprint.route('/by-level/<int:level_id>', methods=['GET'], strict_slashes=False)(token_required(self.get_quiz_by_level_id))
        
        # Create a new quiz (Admin only)
        self.blueprint.route('', methods=['POST'], strict_slashes=False)(admin_required(self.create_quiz))
        
        # Update a quiz (Admin only)
        self.blueprint.route('/<int:quiz_id>', methods=['PUT'], strict_slashes=False)(admin_required(self.update_quiz))

        # Delete a quiz (Admin only)
        self.blueprint.route('/<int:quiz_id>', methods=['DELETE'], strict_slashes=False)(admin_required(self.delete_quiz))

        # Quiz Questions Routes
        self.blueprint.route('/<int:quiz_id>/questions', methods=['GET'], strict_slashes=False)(token_required(self.get_quiz_questions))
        self.blueprint.route('/<int:quiz_id>/questions', methods=['POST'], strict_slashes=False)(admin_required(self.create_quiz_question))
        self.blueprint.route('/questions/<int:quiz_question_id>', methods=['GET'], strict_slashes=False)(token_required(self.get_quiz_question))
        self.blueprint.route('/questions/<int:quiz_question_id>', methods=['PUT'], strict_slashes=False)(admin_required(self.update_quiz_question))
        self.blueprint.route('/questions/<int:quiz_question_id>', methods=['DELETE'], strict_slashes=False)(admin_required(self.delete_quiz_question))


    # --- CRUD operations for Quizzes ---
    def get_all_quizzes(self) -> Tuple[Dict[str, Any], int]:
        """Get all quizzes."""
        quizzes = self.service.get_all_quizzes()
        return self.success_response(data=[quiz.to_dict() for quiz in quizzes])

    def get_quiz(self, quiz_id: int) -> Tuple[Dict[str, Any], int]:
        """Get a specific quiz by its ID."""
        quiz = self.service.get_quiz_by_id(quiz_id)
        if not quiz:
            return self.error_response("Quiz not found", status_code=404)
        return self.success_response(data=quiz.to_dict())

    def get_quiz_by_level_id(self, level_id: int) -> Tuple[Dict[str, Any], int]:
        """Get a quiz associated with a specific level ID."""
        quiz = self.service.get_quiz_by_level_id(level_id)
        if not quiz:
            return self.error_response("Quiz not found for this level ID", status_code=404)
        return self.success_response(data=quiz.to_dict())

    def create_quiz(self) -> Tuple[Dict[str, Any], int]:
        """Create a new quiz."""
        try:
            data = {}
            # Check for multipart/form-data first (used by frontend forms)
            if request.content_type and 'multipart/form-data' in request.content_type:
                data = request.form.to_dict() # Get form fields from FormData
            elif request.is_json: # Fallback to JSON if not multipart
                data = request.get_json()
            else:
                raise BadRequest("Unsupported Content-Type. Expected JSON or multipart/form-data.")

            if not data:
                raise BadRequest("Request body is empty or invalid.")
            
            level_id = data.get('level_id')
            name = data.get('name')
            description = data.get('description')

            # Basic validation
            if not level_id:
                raise BadRequest("Level ID is required.")
            # Check if name is present and not an empty string
            if not name or str(name).strip() == "": 
                raise BadRequest("Quiz name is required.")

            # CORRECTED LINE: Pass the entire 'data' dictionary
            new_quiz = self.service.create_quiz(data) 
            return self.success_response(
                data=new_quiz.to_dict(),
                message="Quiz created successfully",
                status_code=201
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error creating quiz: {e}")
            return self.error_response("Failed to create quiz", status_code=500)

    def update_quiz(self, quiz_id: int) -> Tuple[Dict[str, Any], int]:
        """Update a specific quiz by its ID."""
        try:
            data = {}
            if request.content_type and 'multipart/form-data' in request.content_type:
                data = request.form.to_dict()
            elif request.is_json:
                data = request.get_json()
            else:
                raise BadRequest("Unsupported Content-Type. Expected JSON or multipart/form-data.")
            
            if not data:
                raise BadRequest("Request body is empty or invalid.")
            
            quiz = self.service.update_quiz(quiz_id, data)
            if not quiz:
                return self.error_response("Quiz not found", status_code=404)
            return self.success_response(
                data=quiz.to_dict(),
                message="Quiz updated successfully"
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error updating quiz: {e}")
            return self.error_response("Failed to update quiz", status_code=500)

    def delete_quiz(self, quiz_id: int) -> Tuple[Dict[str, Any], int]:
        """Delete a specific quiz by its ID."""
        try:
            success = self.service.delete_quiz(quiz_id)
            if not success:
                return self.error_response("Quiz not found", status_code=404)
            return self.success_response(message="Quiz deleted successfully")
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error deleting quiz: {e}")
            return self.error_response("Failed to delete quiz", status_code=500)

    # --- CRUD operations for Quiz Questions ---
    def get_quiz_questions(self, quiz_id: int) -> Tuple[Dict[str, Any], int]:
        """Get all questions for a specific quiz."""
        try:
            quiz_questions = self.service.get_quiz_questions_for_quiz(quiz_id)
            return self.success_response(data=[q.to_dict() for q in quiz_questions])
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error getting quiz questions: {e}")
            return self.error_response("Failed to retrieve quiz questions", status_code=500)

    def get_quiz_question(self, quiz_question_id: int) -> Tuple[Dict[str, Any], int]:
        """Get a specific quiz question by its ID."""
        try:
            quiz_question = self.service.get_quiz_question_by_id(quiz_question_id)
            if not quiz_question:
                return self.error_response("Quiz question not found", status_code=404)
            return self.success_response(data=quiz_question.to_dict())
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error getting quiz question: {e}")
            return self.error_response("Failed to retrieve quiz question", status_code=500)

    def create_quiz_question(self, quiz_id: int) -> Tuple[Dict[str, Any], int]:
        """Create a new quiz question for a specific quiz."""
        try:
            if request.content_type and 'multipart/form-data' in request.content_type:
                data = request.form.to_dict() # Get form fields as dict
                files = request.files # Get FileStorage objects
            else:
                data = request.get_json()
                files = None

            new_quiz_question = self.service.create_quiz_question(quiz_id, data, files)
            return self.success_response(
                data=new_quiz_question.to_dict(),
                message="Quiz question created successfully",
                status_code=201
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error creating quiz question: {e}")
            return self.error_response("Failed to create quiz question", status_code=500)

    def delete_quiz_question(self, quiz_question_id: int) -> Tuple[Dict[str, Any], int]:
        """Delete a specific quiz question by its ID."""
        try:
            success = self.service.delete_quiz_question(quiz_question_id)
            if not success:
                return self.error_response("Quiz question not found", status_code=404)
            return self.success_response(message="Quiz question deleted successfully")
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error deleting quiz question: {e}")
            return self.error_response("Failed to delete quiz question", status_code=500)

    def update_quiz_question(self, quiz_question_id: int) -> Tuple[Dict[str, Any], int]:
        """Update a specific quiz question by its ID."""
        try:
            # Handle multipart/form-data for file uploads or application/json
            if request.content_type and 'multipart/form-data' in request.content_type:
                data = request.form.to_dict() # Get form fields as dict
                files = request.files # Get FileStorage objects
                # Note: `data` from request.form will have string values.
                # Booleans/numbers need conversion in service if not handled there.
            else:
                data = request.get_json()
                files = None

            quiz_question = self.service.update_quiz_question(quiz_question_id, data, files)
            if not quiz_question:
                return self.error_response("Quiz question not found", status_code=404)
            return self.success_response(
                data=quiz_question.to_dict(),
                message="Quiz question updated successfully"
            )
        except BadRequest as e:
            return self.error_response(str(e))
        except Exception as e:
            print(f"Error updating quiz question: {e}")
            return self.error_response("Failed to update quiz question", status_code=500)


# Create blueprint instance
quiz_bp = QuizController().blueprint
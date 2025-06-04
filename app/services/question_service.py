import json
from typing import Dict, Any, List, Optional
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import SQLAlchemyError 

# IMPORTANT: Import db from the 'app' package where it's initialized
from app import db 
# Import your models from app.models
from app.models.question import Question, QuestionChoice # Assuming question models are in app/models/question.py
# Import your enums (assuming they are in app.enums)
from app.enums import QuestionType, AnswerType, ChoiceType 
# Import file utility functions
from app.utils.file_upload import save_file, delete_file

# If BaseService is in a different location, adjust its import
# Assuming it's in app.services.base_service
from app.services.base_service import BaseService


class QuestionService(BaseService):
    """Service class for handling question-related operations."""
    
    def __init__(self):
        """Initialize the question service."""
        super().__init__(Question) # Pass the model to BaseService

    def get_all(self) -> List[Question]:
        """Get all questions."""
        return Question.query.all()

    def get_by_id(self, question_id: int) -> Optional[Question]:
        """Get a specific question by ID."""
        return Question.query.get(question_id)

    def get_questions_by_section(self, section_id: int) -> List[Question]:
        """Get questions filtered by section ID."""
        return Question.query.filter_by(section_id=section_id).all()

    def create_question(self, data: Dict[str, Any], question_file: Optional[FileStorage] = None, files: Optional[Dict[str, FileStorage]] = None) -> Question:
        """
        Create a new question, handling different question types and choice uploads.
        'files' parameter is a dict-like object from request.files, used for choice media.
        """
        # Parse choices from data. If it's a string (from multipart form), load it as JSON.
        choices_data = data.get('choices')
        if choices_data and isinstance(choices_data, str):
            try:
                choices_data = json.loads(choices_data)
            except json.JSONDecodeError:
                raise BadRequest("Invalid JSON format for choices.")
        elif not choices_data:
            choices_data = [] # Ensure choices_data is always a list for iteration

        # Validate enums for question_type and answer_type
        try:
            qtype_str = data.get('question_type')
            if not qtype_str:
                raise BadRequest("Missing question_type")
            qtype = QuestionType(qtype_str)

            atype_str = data.get('answer_type')
            if not atype_str:
                raise BadRequest("Missing answer_type")
            atype = AnswerType(atype_str)

        except ValueError as e:
            raise BadRequest(f"Invalid question_type or answer_type: {e}")
        except KeyError as e:
            raise BadRequest(f"Missing required field: {e}")

        # Handle question content file (for IMAGE/AUDIO question types)
        question_content_path = None
        if qtype in [QuestionType.IMAGE, QuestionType.AUDIO]:
            if not question_file:
                raise BadRequest("Question file is required for image/audio question type.")
            question_content_path = save_file(question_file, 'questions') # Save question media
        else:
            question_content_path = data.get('question_content')
            if not question_content_path and qtype == QuestionType.TEXT:
                raise BadRequest("Question content is required for text type questions.")

        # Create the Question object
        question = Question(
            section_id=data.get('section_id'), 
            # Reverted: Pass the Enum member directly, as SQLAlchemy's db.Enum handles conversion
            question_type=qtype, 
            question_content=question_content_path,
            answer_type=atype, 
            correct_answer=None # Initialize to None, set later for FILL_IN_BLANK
        )

        # Handle choices for multiple choice questions
        if atype == AnswerType.MULTIPLE_CHOICE:
            if not choices_data:
                raise BadRequest("Choices are required for multiple-choice questions.")
            
            # --- DEBUGGING STATEMENTS START (create_question) ---
            print(f"\n--- DEBUGGING CHOICES START (create_question) ---")
            print(f"Received choices_data: {choices_data}") 

            has_correct = False # Flag to ensure at least one correct choice

            for idx, choice_dict in enumerate(choices_data):
                print(f"  Processing choice {idx}: {choice_dict}")

                choice_content = choice_dict.get('content')
                if not choice_content or not str(choice_content).strip():
                    raise BadRequest(f"Choice content for choice {idx} cannot be empty.")

                is_correct_val = choice_dict.get('is_correct', False) 
                if isinstance(is_correct_val, str):
                    is_correct_val = is_correct_val.lower() == 'true'
                elif isinstance(is_correct_val, (int, float)):
                    is_correct_val = bool(is_correct_val)
                
                print(f"    is_correct_val (after conversion): {is_correct_val} (type: {type(is_correct_val)})")

                if is_correct_val:
                    has_correct = True
                    print(f"    Choice {idx} is CORRECT! has_correct is now {has_correct}")
                else:
                    print(f"    Choice {idx} is NOT correct.")

                current_choice_type = ChoiceType.TEXT # Using the imported ChoiceType enum

                # Handle file upload for choice content if it's an image/audio choice
                if current_choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                    file_key = choice_dict.get('file_key') 
                    if not file_key:
                        raise BadRequest("Missing file_key for image/audio choice content.")
                    
                    file_obj = files.get(file_key) if files else None
                    if not file_obj:
                        raise BadRequest(f"File for choice '{file_key}' is missing for image/audio type.")
                    
                    choice_content = save_file(file_obj, 'choices') 
                
                new_choice = QuestionChoice(
                    choice_type=current_choice_type, 
                    content=choice_content,
                    is_correct=is_correct_val
                )
                question.choices.append(new_choice) 

            print(f"--- DEBUGGING CHOICES END (create_question) ---")
            print(f"Final has_correct before validation: {has_correct}")

            if not has_correct:
                raise BadRequest("At least one choice must be marked as correct for multiple-choice questions.")

        elif atype == AnswerType.FILL_IN_BLANK:
            correct_answer = data.get('correct_answer')
            if not correct_answer or not str(correct_answer).strip():
                raise BadRequest("Correct answer is required for fill-in-the-blank questions.")
            question.correct_answer = correct_answer
        
        try:
            db.session.add(question)
            db.session.commit() 
            return question
        except SQLAlchemyError as e:
            db.session.rollback() 
            print(f"Database error during question creation: {e}") 
            raise BadRequest(f"Database error during question creation: {str(e)}")


    def update_question(self, question_id: int, data: Dict[str, Any], question_file: Optional[FileStorage] = None, files: Optional[Dict[str, FileStorage]] = None) -> Optional[Question]:
        """Update an existing question."""
        question = self.get_by_id(question_id)
        if not question:
            return None

        db.session.begin_nested() 

        try:
            # Update general question fields
            if 'section_id' in data:
                question.section_id = data['section_id']
            
            if 'question_type' in data:
                try:
                    # Reverted: Pass the Enum member directly
                    question.question_type = QuestionType(data['question_type']) 
                except ValueError:
                    raise BadRequest("Invalid question_type provided.")
            
            if 'answer_type' in data:
                try:
                    # Reverted: Pass the Enum member directly
                    question.answer_type = AnswerType(data['answer_type']) 
                except ValueError:
                    raise BadRequest("Invalid answer_type provided.")

            # Handle question_content based on updated question_type
            if question_file:
                if question.question_content and question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                    delete_file(question.question_content)
                question.question_content = save_file(question_file, 'questions')
            elif 'question_content' in data and question.question_type == QuestionType.TEXT:
                question.question_content = data['question_content']
                if not question.question_content and question.question_type == QuestionType.TEXT:
                    raise BadRequest("Question content is required for text type questions.")
            elif 'question_content' in data and data['question_content'] is None and question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                if question.question_content:
                    delete_file(question.question_content)
                question.question_content = None 

            # Handle choices for multiple choice questions
            if question.answer_type == AnswerType.MULTIPLE_CHOICE:
                if 'choices' not in data:
                    pass 
                else:
                    choices_data = data['choices']
                    if choices_data and isinstance(choices_data, str):
                        try:
                            choices_data = json.loads(choices_data)
                        except json.JSONDecodeError:
                            raise BadRequest("Invalid JSON format for choices.")
                    elif not choices_data:
                        choices_data = []

                    for existing_choice in question.choices:
                        db.session.delete(existing_choice)
                    question.choices.clear() 

                    has_correct = False
                    for idx, choice_dict in enumerate(choices_data):
                        choice_content = choice_dict.get('content')
                        if not choice_content or not str(choice_content).strip():
                            raise BadRequest(f"Choice content for choice {idx} cannot be empty.")

                        is_correct_val = choice_dict.get('is_correct', False)
                        if isinstance(is_correct_val, str):
                            is_correct_val = is_correct_val.lower() == 'true'
                        elif isinstance(is_correct_val, (int, float)):
                            is_correct_val = bool(is_correct_val)
                        
                        if is_correct_val:
                            has_correct = True

                        current_choice_type = ChoiceType.TEXT 

                        if current_choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                            file_key = choice_dict.get('file_key')
                            if file_key and files and files.get(file_key):
                                choice_content = save_file(files.get(file_key), 'choices')
                            pass 

                        new_choice = QuestionChoice(
                            choice_type=current_choice_type,
                            content=choice_content,
                            is_correct=is_correct_val
                        )
                        question.choices.append(new_choice)
                    
                    if not has_correct:
                        raise BadRequest("At least one choice must be marked as correct for multiple-choice questions.")

            elif question.answer_type == AnswerType.FILL_IN_BLANK:
                correct_answer = data.get('correct_answer')
                if not correct_answer or not str(correct_answer).strip():
                    raise BadRequest("Correct answer is required for fill-in-the-blank questions.")
                question.correct_answer = correct_answer
                for existing_choice in question.choices:
                    db.session.delete(existing_choice)
                question.choices.clear()
            else: 
                question.correct_answer = None
                for existing_choice in question.choices:
                    db.session.delete(existing_choice)
                question.choices.clear()


            db.session.add(question) 
            db.session.commit()
            return question
        except BadRequest as e:
            db.session.rollback()
            raise e 
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during question update: {e}")
            raise BadRequest(f"Database error during question update: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error during question update: {e}")
            raise BadRequest(f"An unexpected error occurred: {str(e)}")


    def delete_question(self, question_id: int) -> bool:
        """Delete a question by ID, including associated files."""
        question = self.get_by_id(question_id)
        if not question:
            return False

        try:
            if question.question_content and question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                delete_file(question.question_content)
            
            for choice in question.choices:
                if choice.content and choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                    delete_file(choice.content)
            
            db.session.delete(question)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during question deletion: {e}")
            raise BadRequest(f"Database error during question deletion: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting question or its files: {e}")
            raise BadRequest(f"Failed to delete question: {str(e)}")

    def add_multiple_choices(self, question_id: int, choices_data: List[Dict[str, Any]], files: Optional[Dict[str, FileStorage]] = None) -> List[QuestionChoice]:
        """Add multiple choices to an existing question."""
        question = self.get_by_id(question_id)
        if not question:
            raise BadRequest("Question not found.")
        
        if question.answer_type != AnswerType.MULTIPLE_CHOICE:
            raise BadRequest("Choices can only be added to multiple-choice questions.")

        newly_added_choices = []
        try:
            has_existing_correct = any(c.is_correct for c in question.choices)

            for idx, choice_dict in enumerate(choices_data):
                choice_content = choice_dict.get('content')
                if not choice_content or not str(choice_content).strip():
                    raise BadRequest(f"Choice content for choice {idx} cannot be empty.")

                is_correct_val = choice_dict.get('is_correct', False)
                if isinstance(is_correct_val, str):
                    is_correct_val = is_correct_val.lower() == 'true'
                elif isinstance(is_correct_val, (int, float)):
                    is_correct_val = bool(is_correct_val)
                
                if is_correct_val:
                    has_existing_correct = True 

                current_choice_type = ChoiceType.TEXT 

                if current_choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                    file_key = choice_dict.get('file_key')
                    if not file_key:
                        raise BadRequest("Missing file_key for image/audio choice content.")
                    
                    file_obj = files.get(file_key) if files else None
                    if not file_obj:
                        raise BadRequest(f"File for choice '{file_key}' is missing for image/audio type.")
                    
                    choice_content = save_file(file_obj, 'choices')

                new_choice = QuestionChoice(
                    question_id=question.id, 
                    choice_type=current_choice_type,
                    content=choice_content,
                    is_correct=is_correct_val
                )
                db.session.add(new_choice)
                newly_added_choices.append(new_choice)
            
            if not has_existing_correct:
                db.session.rollback() 
                raise BadRequest("At least one correct choice must exist for multiple-choice questions.")

            db.session.commit()
            return newly_added_choices
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during adding choices: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except BadRequest as e:
            db.session.rollback() 
            raise e
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error adding choices: {e}")
            raise BadRequest(f"An unexpected error occurred while adding choices: {str(e)}")

    def delete_choice(self, question_id: int, choice_id: int) -> bool:
        """Delete a specific choice from a question."""
        choice = QuestionChoice.query.filter_by(id=choice_id, question_id=question_id).first()
        if not choice:
            raise BadRequest("Choice not found for this question.")

        if choice.is_correct and QuestionChoice.query.filter_by(question_id=question_id, is_correct=True).count() == 1:
            raise BadRequest("Cannot delete the last correct choice for a multiple-choice question.")

        try:
            # Delete associated media file if it's a media choice
            if choice.content and choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                delete_file(choice.content)

            db.session.delete(choice)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during choice deletion: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting choice: {e}")
            raise BadRequest(f"Failed to delete choice: {str(e)}")

    def update_single_choice(self, question_id: int, choice_id: int, data: Dict[str, Any], files: Optional[Dict[str, FileStorage]] = None) -> Optional[QuestionChoice]:
        """Update a single choice for a question."""
        choice = QuestionChoice.query.filter_by(id=choice_id, question_id=question_id).first()
        if not choice:
            return None

        try:
            db.session.begin_nested() 

            # Update content
            if 'content' in data:
                new_content = data['content']
                if not new_content or not str(new_content).strip():
                    raise BadRequest("Choice content cannot be empty.")
                choice.content = new_content

            # Update is_correct
            if 'is_correct' in data:
                is_correct_val = data['is_correct']
                if isinstance(is_correct_val, str):
                    is_correct_val = is_correct_val.lower() == 'true'
                elif isinstance(is_correct_val, (int, float)):
                    is_correct_val = bool(is_correct_val)

                # Prevent setting is_correct to False if it's the last correct choice
                if choice.is_correct and not is_correct_val:
                    other_correct_choices_count = QuestionChoice.query.filter(
                        QuestionChoice.question_id == question_id,
                        QuestionChoice.is_correct == True,
                        QuestionChoice.id != choice_id
                    ).count()
                    if other_correct_choices_count == 0:
                        raise BadRequest("Cannot unmark the last correct choice. At least one correct choice is required.")
                choice.is_correct = is_correct_val

            current_choice_type = ChoiceType.TEXT 

            if 'choice_type' in data: 
                try:
                    new_choice_type = ChoiceType(data['choice_type'])
                    if new_choice_type != choice.choice_type:
                        if choice.content and choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                            delete_file(choice.content)
                        choice.choice_type = new_choice_type
                        choice.content = None 

                except ValueError:
                    raise BadRequest("Invalid choice_type provided.")

            if files and 'media' in files: 
                file_obj = files['media']
                if file_obj:
                    if choice.content and choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                        delete_file(choice.content) 
                    choice.content = save_file(file_obj, 'choices') 
                    choice.choice_type = ChoiceType.IMAGE if file_obj.mimetype.startswith('image/') else ChoiceType.AUDIO 

            db.session.add(choice) 
            db.session.commit()
            return choice
        except BadRequest as e:
            db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during choice update: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error during choice update: {e}")
            raise BadRequest(f"An unexpected error occurred: {str(e)}")
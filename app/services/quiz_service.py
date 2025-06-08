# app/services/quiz_service.py

import json
from typing import Dict, Any, List, Optional
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload # Import joinedload for eager loading

from app import db 
from app.models.quiz import Quiz, QuizQuestion, QuizChoice # Import ALL new Quiz models
from app.models.level import Level # Need Level model to fetch level details
# No longer directly importing Question/Section here for quiz questions, as they are separate
from app.enums import QuestionType, AnswerType, ChoiceType 
from app.services.base_service import BaseService 
from app.utils.file_upload import save_file, delete_file # For media content in quiz questions/choices

class QuizService(BaseService):
    """Service class for handling quiz-related operations."""
    
    def __init__(self):
        """Initialize the quiz service."""
        super().__init__(Quiz)

    def get_all_quizzes(self) -> List[Quiz]:
        """Get all quizzes, eagerly loading their questions and choices."""
        return Quiz.query.options(
            joinedload(Quiz.quiz_questions).joinedload(QuizQuestion.quiz_choices)
        ).all()

    def get_quiz_by_id(self, quiz_id: int) -> Optional[Quiz]:
        """Get a quiz by its ID, eagerly loading its questions and choices."""
        return Quiz.query.options(
            joinedload(Quiz.quiz_questions).joinedload(QuizQuestion.quiz_choices)
        ).get(quiz_id)

    def get_quiz_by_level_id(self, level_id: int) -> Optional[Quiz]:
        """Get a quiz associated with a specific level ID, eagerly loading its questions and choices."""
        return Quiz.query.filter_by(level_id=level_id).options(
            joinedload(Quiz.quiz_questions).joinedload(QuizQuestion.quiz_choices)
        ).first()

    def create_quiz(self, data: Dict[str, Any]) -> Quiz:
        """
        Create a new quiz for a given level.
        It will now start with no questions. Quiz-specific questions can be added later
        using the add_or_update_quiz_questions method.
        """
        level_id = data.get('level_id')
        name = data.get('name')
        description = data.get('description')

        if not all([level_id, name]):
            raise BadRequest("Level ID and quiz name are required.")

        existing_quiz = self.get_quiz_by_level_id(level_id)
        if existing_quiz:
            raise BadRequest(f"A quiz already exists for Level ID {level_id}.")

        level = Level.query.get(level_id)
        if not level:
            raise BadRequest(f"Level with ID {level_id} not found.")

        quiz = Quiz(
            level_id=level_id,
            name=name,
            description=description
        )

        try:
            db.session.add(quiz)
            db.session.commit()
            return quiz
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during quiz creation: {e}")
            raise BadRequest(f"Database error during quiz creation: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error during quiz creation: {e}")
            raise BadRequest(f"An unexpected error occurred: {str(e)}")

    def update_quiz(self, quiz_id: int, data: Dict[str, Any]) -> Optional[Quiz]:
        """Update an existing quiz."""
        quiz = self.get_quiz_by_id(quiz_id) # Use get_quiz_by_id to fetch
        if not quiz:
            return None

        db.session.begin_nested()
        try:
            if 'name' in data:
                quiz.name = data['name']
            if 'description' in data:
                quiz.description = data['description']

            if 'level_id' in data and quiz.level_id != data['level_id']:
                existing_quiz_for_new_level = self.get_quiz_by_level_id(data['level_id'])
                if existing_quiz_for_new_level and existing_quiz_for_new_level.id != quiz_id:
                    raise BadRequest(f"A quiz already exists for target Level ID {data['level_id']}.")
                level = Level.query.get(data['level_id'])
                if not level:
                    raise BadRequest(f"Level with ID {data['level_id']} not found.")
                quiz.level_id = data['level_id']

            db.session.add(quiz)
            db.session.commit()
            return quiz
        except BadRequest as e:
            db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during quiz update: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error during quiz update: {e}")
            raise BadRequest(f"An unexpected error occurred: {str(e)}")

    def delete_quiz(self, quiz_id: int) -> bool:
        """Delete a quiz by ID, including its specific questions and choices."""
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            return False

        try:
            # Due to `cascade='all, delete-orphan'` on `quiz_questions` relationship in Quiz model,
            # deleting the quiz will cascade delete all associated QuizQuestion and QuizChoice entries.
            db.session.delete(quiz)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during quiz deletion: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting quiz: {e}")
            raise BadRequest(f"Failed to delete quiz: {str(e)}")

    def _prepare_quiz_question_for_addition(self, quiz_id: int, question_data: Dict[str, Any], order_in_quiz: int, files: Optional[Dict[str, Any]] = None) -> QuizQuestion:
        """
        Helper method to prepare a single QuizQuestion object for addition to the session.
        Handles nested choices and file uploads for quiz questions.
        Does NOT commit the session.
        """
        question_content_val = question_data.get('question_content')
        
        # Note: handler.js hardcodes question_type to 'text'.
        # This implies question_content_val is always text.
        # The logic below for IMAGE/AUDIO question_type will not be hit if handler.js isn't updated.
        qtype = QuestionType(question_data.get('question_type')) # Should be QuestionType.TEXT from handler.js

        # Handle question content file upload for quiz questions if question_type was IMAGE/AUDIO
        # (This part is only relevant if handler.js allows setting question_type to IMAGE/AUDIO and sending a file)
        if qtype in [QuestionType.IMAGE, QuestionType.AUDIO]:
            file_key = question_data.get('file_key') # Expect file_key for FormData
            if not file_key or not (files and file_key in files):
                raise BadRequest(f"Question file (via file_key '{file_key}') is required for image/audio quiz question type.")
            question_content_val = save_file(files[file_key], 'quiz_questions') # Save quiz question media
        elif not question_content_val and qtype == QuestionType.TEXT:
            raise BadRequest("Question content is required for text quiz questions.")


        atype = AnswerType(question_data.get('answer_type'))

        quiz_question = QuizQuestion(
            quiz_id=quiz_id,
            question_type=qtype, # This will be QuestionType.TEXT due to handler.js
            question_content=question_content_val,
            answer_type=atype,
            correct_answer=question_data.get('correct_answer'),
            order_in_quiz=order_in_quiz
        )
        db.session.add(quiz_question)
        db.session.flush() # Flush to get quiz_question.id for QuizChoice association

        # Handle choices for multiple choice quiz questions
        if atype == AnswerType.MULTIPLE_CHOICE:
            choices_data = question_data.get('choices')
            if not choices_data or not isinstance(choices_data, list):
                raise BadRequest("Choices are required for multiple-choice quiz questions.")
            
            has_correct = False
            for choice_dict in choices_data:
                choice_content_val = choice_dict.get('content')
                
                # Ensure choice_type is handled, defaulting to TEXT if not explicitly set
                choice_type = ChoiceType(choice_dict.get('choice_type', 'text')) 

                if not choice_content_val and choice_type == ChoiceType.TEXT:
                    raise BadRequest("Choice content is required for text quiz choices.")
                
                is_correct_val = choice_dict.get('is_correct', False)
                if isinstance(is_correct_val, str): is_correct_val = is_correct_val.lower() == 'true'

                # Handle choice content file upload for quiz choices
                if choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                    choice_file_key = choice_dict.get('file_key')
                    if not choice_file_key or not (files and choice_file_key in files):
                        raise BadRequest(f"Choice file (via file_key '{choice_file_key}') is required for image/audio quiz choice type.")
                    choice_content_val = save_file(files[choice_file_key], 'quiz_choices') # Save quiz choice media

                new_quiz_choice = QuizChoice(
                    quiz_question_id=quiz_question.id,
                    choice_type=choice_type,
                    content=choice_content_val,
                    is_correct=is_correct_val
                )
                db.session.add(new_quiz_choice)
                if is_correct_val:
                    has_correct = True
            
            if not has_correct:
                raise BadRequest("At least one choice must be marked as correct for multiple-choice quiz questions.")
        
        elif atype == AnswerType.FILL_IN_BLANK:
            if not question_data.get('correct_answer'):
                raise BadRequest("Correct answer is required for fill-in-the-blank quiz questions.")
            quiz_question.correct_answer = question_data.get('correct_answer')
            
        return quiz_question

    def create_quiz_question(self, quiz_id: int, question_data: Dict[str, Any], files: Optional[Dict[str, Any]] = None) -> QuizQuestion:
        """
        Create a new quiz question for a specific quiz.
        This is the method called directly by quiz_controller.
        """
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise BadRequest(f"Quiz with ID {quiz_id} not found.")

        order_in_quiz = question_data.get('order_in_quiz')
        if order_in_quiz is None:
            # If order_in_quiz is not provided, determine the next sequential order
            order_in_quiz = QuizQuestion.query.filter_by(quiz_id=quiz_id).count() + 1
        else:
            try:
                order_in_quiz = int(order_in_quiz)
            except ValueError:
                raise BadRequest("Order in quiz must be an integer.")

        try:
            # Use the helper to prepare the question and its choices
            quiz_question = self._prepare_quiz_question_for_addition(quiz_id, question_data, order_in_quiz, files)
            
            db.session.commit() # Commit the changes here for single question creation
            return quiz_question
        except BadRequest as e:
            db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during single quiz question creation: {e}")
            raise BadRequest(f"Database error during single quiz question creation: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error during single quiz question creation: {e}")
            raise BadRequest(f"An unexpected error occurred during single quiz question creation: {str(e)}")

    def add_or_update_quiz_questions(self, quiz_id: int, questions_data: List[Dict[str, Any]], files: Optional[Dict[str, Any]] = None) -> Quiz:
        """
        Adds new quiz-specific questions to a quiz or updates existing ones.
        This method replaces all existing quiz questions with the provided list.
        It expects a list of question data dictionaries.
        """
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            raise BadRequest("Quiz not found.")
        
        if not questions_data or len(questions_data) == 0:
            raise BadRequest("At least one quiz question must be provided.")
        
        if len(questions_data) != 10:
            print(f"Warning: Expected 10 quiz questions, but received {len(questions_data)}. Adding/updating available.")


        db.session.begin_nested() # Use nested transaction for bulk operations
        try:
            # Clear existing quiz questions for simplicity, then add new ones
            for existing_qq in quiz.quiz_questions:
                # If question had media content, delete its file
                if existing_qq.question_content and existing_qq.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                    delete_file(existing_qq.question_content)
                # If question had choices with media, delete their files
                if existing_qq.answer_type == AnswerType.MULTIPLE_CHOICE:
                    for choice in existing_qq.quiz_choices:
                        if choice.content and choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                            delete_file(choice.content)
                db.session.delete(existing_qq)
            quiz.quiz_questions.clear() # Clear relationship collection in Python
            db.session.flush() # Flush to apply deletions before adding new ones

            # Create new quiz questions and their choices
            for i, question_dict in enumerate(questions_data):
                # Use the helper to prepare the question for bulk addition
                self._prepare_quiz_question_for_addition(quiz.id, question_dict, i + 1, files)
            
            db.session.commit()
            return quiz
        except BadRequest as e:
            db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error adding/updating quiz questions: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error adding/updating quiz questions: {e}")
            raise BadRequest(f"An unexpected error occurred: {str(e)}")

    def delete_quiz_question(self, quiz_question_id: int) -> bool:
        """Delete a specific quiz question and its choices."""
        quiz_question = QuizQuestion.query.get(quiz_question_id)
        if not quiz_question:
            raise BadRequest("Quiz question not found.")

        try:
            # Delete associated media files for the question
            if quiz_question.question_content and quiz_question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                delete_file(quiz_question.question_content)
            
            # Delete associated media files for its choices
            for choice in quiz_question.quiz_choices:
                if choice.content and choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                    delete_file(choice.content)

            db.session.delete(quiz_question)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during quiz question deletion: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting quiz question: {e}")
            raise BadRequest(f"Failed to delete quiz question: {str(e)}")
            
    def update_quiz_question(self, quiz_question_id: int, data: Dict[str, Any], files: Optional[Dict[str, Any]] = None) -> Optional[QuizQuestion]:
        """Update a specific quiz question."""
        quiz_question = QuizQuestion.query.get(quiz_question_id)
        if not quiz_question:
            return None

        db.session.begin_nested()
        try:
            if 'question_type' in data:
                old_qtype = quiz_question.question_type
                quiz_question.question_type = QuestionType(data['question_type'])
                if old_qtype in [QuestionType.IMAGE, QuestionType.AUDIO] and quiz_question.question_type not in [QuestionType.IMAGE, QuestionType.AUDIO]:
                    if quiz_question.question_content: delete_file(quiz_question.question_content)
                    quiz_question.question_content = None # Clear old media path

            if 'question_content' in data:
                if quiz_question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                    # This implies file upload, handled below
                    pass 
                else: # Text content
                    if not data['question_content']: raise BadRequest("Question content cannot be empty for text type.")
                    quiz_question.question_content = data['question_content']
            elif 'question_content' in data and data['question_content'] is None and quiz_question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                if quiz_question.question_content: delete_file(quiz_question.question_content)
                quiz_question.question_content = None

            if 'answer_type' in data:
                quiz_question.answer_type = AnswerType(data['answer_type'])

            if 'correct_answer' in data:
                if quiz_question.answer_type == AnswerType.FILL_IN_BLANK and not data['correct_answer']:
                    raise BadRequest("Correct answer is required for fill-in-the-blank questions.")
                quiz_question.correct_answer = data['correct_answer']

            if 'order_in_quiz' in data:
                quiz_question.order_in_quiz = data['order_in_quiz']

            # Handle question_content file if new file provided
            if files and 'question_file' in files: # Assuming the file is sent with key 'question_file'
                if quiz_question.question_content and quiz_question.question_type in [QuestionType.IMAGE, QuestionType.AUDIO]:
                    delete_file(quiz_question.question_content)
                quiz_question.question_content = save_file(files['question_file'], 'quiz_questions')
                # Update question_type if it changed based on the new file type
                if not quiz_question.question_type or (quiz_question.question_type not in [QuestionType.IMAGE, QuestionType.AUDIO]):
                    quiz_question.question_type = QuestionType.IMAGE if files['question_file'].mimetype.startswith('image/') else QuestionType.AUDIO


            # Handle choices if present (for multiple choice quiz questions)
            if 'choices' in data and quiz_question.answer_type == AnswerType.MULTIPLE_CHOICE:
                new_choices_data = data['choices']
                if not isinstance(new_choices_data, list):
                    raise BadRequest("Choices must be a list of choice objects.")
                
                # Clear existing choices
                for existing_choice in quiz_question.quiz_choices:
                    if existing_choice.content and existing_choice.choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO]:
                        delete_file(existing_choice.content)
                    db.session.delete(existing_choice)
                quiz_question.quiz_choices.clear()
                db.session.flush()

                has_correct = False
                for choice_dict in new_choices_data:
                    choice_content_val = choice_dict.get('content')
                    is_correct_val = choice_dict.get('is_correct', False)
                    if isinstance(is_correct_val, str): is_correct_val = is_correct_val.lower() == 'true'

                    choice_type = ChoiceType(choice_dict.get('choice_type', 'text')) # Default to text if not provided

                    # Handle choice file if provided in `files`
                    choice_file_key = choice_dict.get('file_key')
                    if choice_type in [ChoiceType.IMAGE, ChoiceType.AUDIO] and choice_file_key and files and choice_file_key in files:
                        choice_content_val = save_file(files[choice_file_key], 'quiz_choices')
                    elif not choice_content_val and choice_type == ChoiceType.TEXT:
                        raise BadRequest("Choice content is required for text quiz choices.")
                    
                    new_quiz_choice = QuizChoice(
                        quiz_question_id=quiz_question.id,
                        choice_type=choice_type,
                        content=choice_content_val,
                        is_correct=is_correct_val
                    )
                    db.session.add(new_quiz_choice)
                    if is_correct_val: has_correct = True
                
                if not has_correct:
                    raise BadRequest("At least one choice must be marked as correct for multiple-choice quiz questions.")
            
            db.session.add(quiz_question)
            db.session.commit()
            return quiz_question
        except BadRequest as e:
            db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during quiz question update: {e}")
            raise BadRequest(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error during quiz question update: {e}")
            raise BadRequest(f"An unexpected error occurred: {str(e)}")
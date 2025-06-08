# app/models/quiz.py

from app import db # Import the db instance from the main app package
from datetime import datetime
from sqlalchemy import UniqueConstraint
import enum # Needed for the new Enum definitions in this file

# Importing existing models for relationships if needed (Level is still relevant)
from app.models.question import Question # Keep this if you need to reference original Questions (e.g., in other parts)

# --- NEW/REVISED ENUM FOR QUIZ QUESTIONS' ANSWER TYPE ---
# We can use the same logic for QuestionType and ChoiceType if they apply.
# Let's import from central enums.py for consistency where possible.
from app.enums import QuestionType, ChoiceType

# It's good practice to reuse the AnswerType from enums if it's the same,
# but for quiz-specific questions, if the answer types were different,
# you might define a new Enum here. Assuming they are the same for now.
from app.enums import AnswerType # Reusing the central AnswerType

class Quiz(db.Model):
    """
    Represents a quiz, which is associated with a specific level.
    Each level can have one quiz.
    """
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the Level model. Each quiz is tied to a level.
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False, unique=True) # Unique per level
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    level = db.relationship('Level', backref='quiz', uselist=False) # One-to-one relationship with Level

    # One-to-many relationship with QuizQuestion.
    # 'cascade' ensures that when a Quiz is deleted, its associated QuizQuestions are also deleted.
    # 'order_by' ensures questions are always retrieved in order.
    quiz_questions = db.relationship(
        'QuizQuestion',
        back_populates='quiz',
        cascade='all, delete-orphan',
        order_by='QuizQuestion.order_in_quiz'
    )

    def to_dict(self):
        """Returns a dictionary representation of the quiz."""
        return {
            'id': self.id,
            'level_id': self.level_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'quiz_questions': [q.to_dict() for q in self.quiz_questions] # Include serialized quiz questions
        }


class QuizQuestion(db.Model):
    """
    Represents a specific question within a quiz.
    These are distinct from general 'Question' models and are tied directly to a Quiz.
    """
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the Quiz model
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    
    # Using the QuestionType enum from app.enums (e.g., TEXT, IMAGE, AUDIO, VIDEO)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    question_content = db.Column(db.Text, nullable=False) # The question text or URL to media
    
    # Using the AnswerType enum from app.enums (e.g., MULTIPLE_CHOICE, FILL_IN_BLANK, IMAGE_VIDEO)
    answer_type = db.Column(db.Enum(AnswerType), nullable=False)
    correct_answer = db.Column(db.Text, nullable=True) # For FILL_IN_BLANK or direct answer for other types
    
    order_in_quiz = db.Column(db.Integer, nullable=False) # Order of the question within the quiz
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # Bidirectional relationship with Quiz
    quiz = db.relationship('Quiz', back_populates='quiz_questions')

    # One-to-many relationship with QuizChoice for multiple-choice questions.
    quiz_choices = db.relationship(
        'QuizChoice',
        back_populates='quiz_question',
        cascade='all, delete-orphan',
        order_by='QuizChoice.id' # Or a specific order if choices have one
    )

    # Ensure uniqueness of order_in_quiz within a specific quiz
    __table_args__ = (UniqueConstraint('quiz_id', 'order_in_quiz', name='_quiz_id_order_in_quiz_uc'),)

    def to_dict(self):
        """Returns a dictionary representation of the quiz question."""
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_type': self.question_type.value,
            'question_content': self.question_content,
            'answer_type': self.answer_type.value,
            'correct_answer': self.correct_answer,
            'order_in_quiz': self.order_in_quiz,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'choices': [choice.to_dict() for choice in self.quiz_choices]
        }


class QuizChoice(db.Model):
    """
    Represents a choice for a quiz-specific multiple-choice question.
    """
    __tablename__ = 'quiz_choices'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the QuizQuestion model
    quiz_question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    
    # Using the ChoiceType enum from app.enums
    choice_type = db.Column(db.Enum(ChoiceType), nullable=False) # e.g., TEXT, IMAGE, AUDIO
    content = db.Column(db.String(255), nullable=False) # The choice text or media URL
    is_correct = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # Bidirectional relationship with QuizQuestion
    quiz_question = db.relationship('QuizQuestion', back_populates='quiz_choices')

    def to_dict(self):
        """Returns a dictionary representation of the quiz choice."""
        return {
            'id': self.id,
            'quiz_question_id': self.quiz_question_id,
            'choice_type': self.choice_type.value,
            'content': self.content,
            'is_correct': self.is_correct,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
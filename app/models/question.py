from app import db
from datetime import datetime
import enum
# D:\Graduation Project (1)\Back-End Development Code\app\models\question.py
# import enum # You can remove this if no other enum operations need it directly
from app.enums import QuestionType, AnswerType, ChoiceType # <--- ADD THESE LINES!

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    section = db.relationship('Section', back_populates='questions')
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    question_content = db.Column(db.String(255), nullable=False)
    answer_type = db.Column(db.Enum(AnswerType), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    choices = db.relationship('QuestionChoice', back_populates='question', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'question_type': self.question_type.value,
            'question_content': self.question_content,
            'answer_type': self.answer_type.value,
            'correct_answer': self.correct_answer,
            'choices': [choice.to_dict() for choice in self.choices],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def get_correct_answers(self):
        """ Get the correct answer(s) for the question. """
        if self.answer_type == AnswerType.MULTIPLE_CHOICE:
            return [choice.id for choice in self.choices if choice.is_correct]
        return self.correct_answer

class QuestionChoice(db.Model):
    __tablename__ = 'question_choices'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    choice_type = db.Column(db.Enum(ChoiceType), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    question = db.relationship('Question', back_populates='choices')

    def to_dict(self):
        return {
            'id': self.id,
            'choice_type': self.choice_type.value,
            'content': self.content,
            'is_correct': self.is_correct,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
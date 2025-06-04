# D:\Graduation Project (1)\Back-End Development Code\app\enums.py
from enum import Enum

class QuestionType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    # Add any other question types you might have or plan to have

class AnswerType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"
    IMAGE_VIDEO = "image_video"
    # Add any other answer types

class ChoiceType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    # Add any other choice types
"""
Sistema de preguntas compartido entre módulos.
Permite reutilizar preguntas comunes sin duplicar código.
"""
from .common_questions import CommonQuestions
from .question_builder import QuestionBuilder

__all__ = ['CommonQuestions', 'QuestionBuilder']

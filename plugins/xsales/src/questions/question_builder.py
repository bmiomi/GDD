"""
Constructor de preguntas personalizadas para módulos específicos.
"""
from typing import List, Callable, Any
from .common_questions import QuestionData


class QuestionBuilder:
    """
    Constructor fluido para crear flujos de preguntas personalizados.
    
    Uso:
        builder = QuestionBuilder(context.questionary)
        data = (builder
                .ask_turno(turnos)
                .ask_custom("¿Validar maestros?", ["Sí", "No"])
                .ask_distribuidores(dzs)
                .build())
    """
    
    def __init__(self, questionary):
        self.questionary = questionary
        self._data = QuestionData()
        self._custom_answers = {}
    
    def ask_turno(self, choices: List[str]) -> 'QuestionBuilder':
        """Agrega pregunta de turno al flujo"""
        from .common_questions import CommonQuestions
        self._data.turno = CommonQuestions.ask_turno(self.questionary, choices)
        return self
    
    def ask_proceso(self, choices: List[str]) -> 'QuestionBuilder':
        """Agrega pregunta de proceso al flujo"""
        from .common_questions import CommonQuestions
        self._data.opcion = CommonQuestions.ask_proceso(self.questionary, choices)
        return self
    
    def ask_distribuidores(self, choices: List[str], mensaje: str = None) -> 'QuestionBuilder':
        """Agrega pregunta de distribuidores al flujo"""
        from .common_questions import CommonQuestions
        msg = mensaje or 'Seleccione distribuidores'
        self._data.distribuidores = CommonQuestions.ask_distribuidores(
            self.questionary, choices, msg
        )
        return self
    
    def ask_reporte(self, mensaje: str = None) -> 'QuestionBuilder':
        """Agrega pregunta de reporte al flujo"""
        from .common_questions import CommonQuestions
        msg = mensaje or '¿Desea generar un Excel con la información?'
        self._data.generar_reporte = CommonQuestions.ask_generar_reporte(
            self.questionary, msg
        )
        return self
    
    def ask_custom(self, key: str, mensaje: str, choices: List[str]) -> 'QuestionBuilder':
        """
        Agrega pregunta personalizada al flujo.
        
        Args:
            key: Clave para almacenar la respuesta
            mensaje: Mensaje de la pregunta
            choices: Opciones disponibles
        
        Returns:
            Builder para encadenar más preguntas
        """
        answer = self.questionary.rawselect(mensaje, choices=choices).ask()
        self._custom_answers[key] = answer
        return self
    
    def ask_confirm(self, key: str, mensaje: str) -> 'QuestionBuilder':
        """
        Agrega pregunta de confirmación personalizada.
        
        Args:
            key: Clave para almacenar la respuesta
            mensaje: Mensaje de confirmación
        
        Returns:
            Builder para encadenar más preguntas
        """
        answer = self.questionary.confirm(mensaje).ask()
        self._custom_answers[key] = answer
        return self
    
    def ask_if(self, condition: bool, 
               question_func: Callable[['QuestionBuilder'], 'QuestionBuilder']) -> 'QuestionBuilder':
        """
        Pregunta condicional.
        
        Args:
            condition: Si True, ejecuta la pregunta
            question_func: Función que agrega la pregunta
        
        Returns:
            Builder para encadenar más preguntas
        """
        if condition:
            return question_func(self)
        return self
    
    def build(self) -> tuple[QuestionData, dict]:
        """
        Construye y retorna los datos de las preguntas.
        
        Returns:
            Tupla (QuestionData, respuestas_custom)
        """
        return self._data, self._custom_answers

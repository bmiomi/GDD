"""
Preguntas comunes reutilizables entre módulos.
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class QuestionData:
    """Resultado de las preguntas al usuario"""
    turno: Optional[str] = None
    opcion: Optional[str] = None
    distribuidores: Optional[List[str]] = None
    generar_reporte: bool = False
    dato_extra: Optional[str] = None


class CommonQuestions:
    """
    Preguntas compartidas entre módulos.
    
    Cada módulo puede usar estas preguntas base y extenderlas
    con sus propias preguntas específicas.
    """

    BACK_OPTION = "<< Volver"
    
    @staticmethod
    def ask_turno(questionary, choices: List[str]) -> str:
        """
        Pregunta el turno de trabajo.
        
        Args:
            questionary: Instancia de questionary del contexto
            choices: Lista de turnos disponibles
        
        Returns:
            Turno seleccionado
        """
        choices_with_back = list(choices) + [CommonQuestions.BACK_OPTION]
        selected = questionary.rawselect(
            'Selecciona el turno que te toca',
            choices=choices_with_back
        ).ask()
        if selected == CommonQuestions.BACK_OPTION:
            return None
        return selected
    
    @staticmethod
    def ask_proceso(questionary, choices: List[str]) -> str:
        """
        Pregunta el proceso a realizar.
        
        Args:
            questionary: Instancia de questionary del contexto
            choices: Lista de procesos disponibles (depende del módulo)
        
        Returns:
            Proceso seleccionado
        """
        choices_with_back = list(choices) + [CommonQuestions.BACK_OPTION]
        selected = questionary.rawselect(
            'Seleccione el proceso a realizar',
            choices=choices_with_back
        ).ask()
        if selected == CommonQuestions.BACK_OPTION:
            return None
        return selected
    
    @staticmethod
    def ask_distribuidores(
        questionary,
        choices: List[str],
        mensaje: str = 'Seleccione distribuidores',
        validate=None
    ) -> List[str]:
        """
        Pregunta qué distribuidores procesar.
        
        Args:
            questionary: Instancia de questionary del contexto
            choices: Lista de distribuidores disponibles
            mensaje: Mensaje personalizado (opcional)
        
        Returns:
            Lista de distribuidores seleccionados
        """
        choices_with_back = list(choices) + [CommonQuestions.BACK_OPTION]
        selected = questionary.checkbox(
            mensaje,
            choices=choices_with_back,
            validate=validate
        ).ask()
        if not selected:
            return selected
        if CommonQuestions.BACK_OPTION in selected:
            return None
        return selected
    
    @staticmethod
    def ask_generar_reporte(questionary, mensaje: str = '¿Desea generar un Excel con la información?') -> bool:
        """
        Pregunta si generar reporte.
        
        Args:
            questionary: Instancia de questionary del contexto
            mensaje: Mensaje personalizado (opcional)
        
        Returns:
            True si el usuario quiere generar reporte
        """
        return questionary.confirm(mensaje).ask()
    
    @staticmethod
    def ask_basic_flow(questionary, turnos: List[str], procesos: List[str], 
                       distribuidores: List[str]) -> QuestionData:
        """
        Flujo básico de preguntas (turno → proceso → distribuidores → reporte).
        
        Args:
            questionary: Instancia de questionary
            turnos: Lista de turnos
            procesos: Lista de procesos del módulo
            distribuidores: Lista de distribuidores
        
        Returns:
            QuestionData con las respuestas
        """
        turno = CommonQuestions.ask_turno(questionary, turnos)
        proceso = CommonQuestions.ask_proceso(questionary, procesos)
        dzs = CommonQuestions.ask_distribuidores(questionary, distribuidores)
        reporte = CommonQuestions.ask_generar_reporte(questionary)
        
        return QuestionData(
            turno=turno,
            opcion=proceso,
            distribuidores=dzs,
            generar_reporte=reporte
        )

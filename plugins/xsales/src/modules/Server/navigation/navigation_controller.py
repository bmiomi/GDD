"""
NavigationController: Maneja flujo de navegación entre pantallas.
"""
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class NavigationController:
    """
    Controla la navegación entre pantallas/menús.
    
    Ejemplo:
        navigator = NavigationController()
        
        while True:
            screen = navigator.get_current()
            
            if screen == "main_menu":
                action = show_main_menu()
                if action == "Configurar":
                    navigator.navigate_to("configure_menu")
                    
            elif screen == "configure_menu":
                action = show_configure_menu()
                if action == "Volver":
                    navigator.go_back()  # ← Vuelve a main_menu
    """
    
    def __init__(self):
        """Inicializa el controlador con la pantalla principal."""
        self.screen_stack: List[str] = ["main_menu"]
        logger.debug(f"NavigationController initialized with stack: {self.screen_stack}")
    
    def get_current(self) -> str:
        """
        Obtiene la pantalla actual.
        
        Returns:
            Nombre de la pantalla actual (ej: "main_menu")
        """
        return self.screen_stack[-1] if self.screen_stack else "main_menu"
    
    def navigate_to(self, screen: str) -> None:
        """
        Navega a una nueva pantalla.
        
        Agrega la pantalla al stack (permite volver después).
        
        Args:
            screen: Nombre de la pantalla (ej: "configure_menu")
        """
        self.screen_stack.append(screen)
        logger.debug(f"Navigated to: {screen}, stack: {self.screen_stack}")
    
    def go_back(self) -> str:
        """
        Retrocede a la pantalla anterior.
        
        Returns:
            Nombre de la pantalla anterior
            
        Raises:
            ValueError: Si ya está en la pantalla principal
        """
        if len(self.screen_stack) <= 1:
            logger.warning("Cannot go back from main_menu")
            return self.get_current()
        
        self.screen_stack.pop()
        current = self.get_current()
        logger.debug(f"Went back to: {current}, stack: {self.screen_stack}")
        return current
    
    def reset(self) -> None:
        """Vuelve a la pantalla principal."""
        self.screen_stack = ["main_menu"]
        logger.debug("Navigated to main_menu (reset)")
    
    def get_stack(self) -> List[str]:
        """
        Obtiene el stack de navegación (para debugging).
        
        Returns:
            Lista de pantallas en el stack
        """
        return self.screen_stack.copy()

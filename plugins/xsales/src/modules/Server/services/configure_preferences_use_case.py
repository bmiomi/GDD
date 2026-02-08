"""
Use Case: Configurar preferencias (para ServerModule).
"""
from core.domain import Preferences
from core.repositories import PreferencesRepository


class ConfigurePreferencesUseCase:
    """Gestiona las preferencias de un módulo."""
    
    def __init__(self, prefs_repo: PreferencesRepository):
        self.prefs_repo = prefs_repo
    
    def load(self, module_name: str) -> Preferences:
        """Carga preferencias de un módulo."""
        return self.prefs_repo.load(module_name)
    
    def save(self, module_name: str, preferences: Preferences) -> bool:
        """Guarda preferencias de un módulo."""
        return self.prefs_repo.save(module_name, preferences)
    
    def exists(self, module_name: str) -> bool:
        """¿Existen preferencias guardadas?"""
        return self.prefs_repo.exists(module_name)

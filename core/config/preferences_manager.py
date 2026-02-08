"""
Gestor de preferencias persistentes en YAML.
"""
import os
from pathlib import Path
from typing import Optional
import yaml

from core.models import PreferenceData


class PreferencesManager:
    """Carga/guarda preferencias en YAML."""
    
    def __init__(self, config_dir: str = './config'):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_prefs_file(self, module_name: str) -> Path:
        """Ruta del archivo de preferencias."""
        return self.config_dir / f"{module_name}_preferences.yml"
    
    def load(self, module_name: str) -> Optional[PreferenceData]:
        """Cargar preferencias de YAML."""
        file = self._get_prefs_file(module_name)
        
        if not file.exists():
            return None
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return PreferenceData.from_dict(data or {})
        except Exception as e:
            print(f"Error cargando preferencias: {e}")
            return None
    
    def save(self, module_name: str, prefs: PreferenceData) -> bool:
        """Guardar preferencias en YAML."""
        file = self._get_prefs_file(module_name)
        
        try:
            with open(file, 'w', encoding='utf-8') as f:
                yaml.dump(prefs.to_dict(), f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"Error guardando preferencias: {e}")
            return False
    
    def exists(self, module_name: str) -> bool:
        """¿Existen preferencias guardadas?"""
        return self._get_prefs_file(module_name).exists()

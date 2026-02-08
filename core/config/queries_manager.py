"""
Gestor de consultas personalizadas en YAML.
"""
from pathlib import Path
from typing import List, Optional, Dict
import yaml

from core.models import QueryData


class QueriesManager:
    """Carga/guarda consultas personalizadas en YAML."""
    
    def __init__(self, config_dir: str = './config'):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_queries_file(self, module_name: str) -> Path:
        """Ruta del archivo de consultas."""
        return self.config_dir / f"{module_name}_queries.yml"
    
    def load_all(self, module_name: str) -> Dict[str, QueryData]:
        """Cargar todas las consultas personalizadas."""
        file = self._get_queries_file(module_name)
        
        if not file.exists():
            return {}
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            return {
                name: QueryData.from_dict(name, query_data)
                for name, query_data in data.items()
            }
        except Exception as e:
            print(f"Error cargando consultas: {e}")
            return {}
    
    def load(self, module_name: str, query_name: str) -> Optional[QueryData]:
        """Cargar una consulta específica."""
        queries = self.load_all(module_name)
        return queries.get(query_name)
    
    def save(self, module_name: str, query: QueryData) -> bool:
        """Guardar una consulta personalizada."""
        file = self._get_queries_file(module_name)
        
        try:
            # Cargar queries existentes
            queries = self.load_all(module_name)
            
            # Agregar/actualizar
            queries[query.name] = query
            
            # Guardar todo
            data = {name: q.to_dict() for name, q in queries.items()}
            
            with open(file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"Error guardando consulta: {e}")
            return False
    
    def delete(self, module_name: str, query_name: str) -> bool:
        """Eliminar una consulta personalizada."""
        file = self._get_queries_file(module_name)
        
        try:
            queries = self.load_all(module_name)
            
            if query_name in queries:
                del queries[query_name]
            
            data = {name: q.to_dict() for name, q in queries.items()}
            
            with open(file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"Error eliminando consulta: {e}")
            return False
    
    def exists(self, module_name: str) -> bool:
        """¿Existen consultas personalizar?"""
        return self._get_queries_file(module_name).exists() and bool(self.load_all(module_name))

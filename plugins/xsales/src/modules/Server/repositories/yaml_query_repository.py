"""
Implementación YAML de QueryRepository para ServerModule.
Lee consultas desde config.yml
"""
import yaml
from typing import List, Optional
from pathlib import Path
from ..domain import Query
from core.domain import QueryNotFoundError


class YamlQueryRepository:
    """Accede a consultas desde YAML."""
    
    def __init__(self, config_path: str):
        """
        Args:
            config_path: Ruta al config.yml con consultas
        """
        self.config_path = Path(config_path)
        self._queries: dict = {}
        self._load()
    
    def _load(self):
        """Carga las consultas del YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not config:
            self._queries = {}
            return
        
        # Buscar consultas en diferentes ubicaciones posibles
        consultas = None
        
        # Opción 1: Server.Consultas (estructura actual)
        if 'Server' in config and 'Consultas' in config['Server']:
            consultas = config['Server']['Consultas']
        # Opción 2: Server.consultas (minúscula)
        elif 'Server' in config and 'consultas' in config['Server']:
            consultas = config['Server']['consultas']
        # Opción 3: consultas (minúscula en raíz)
        elif 'consultas' in config:
            consultas = config['consultas']
        
        if not consultas:
            self._queries = {}
            return
        
        # Convertir cada entrada YAML a objeto Query
        for name, data in consultas.items():
            try:
                self._queries[name] = Query.from_dict(name, data)
            except Exception as e:
                raise ValueError(f"Error cargando consulta '{name}': {e}")
    
    def get(self, name: str) -> Query:
        """Obtiene una consulta por nombre."""
        if name not in self._queries:
            raise QueryNotFoundError(query_name=name)
        return self._queries[name]
    
    def list_all(self) -> List[Query]:
        """Lista todas las consultas."""
        return list(self._queries.values())
    
    def save(self, query: Query) -> bool:
        """
        Guarda una consulta en YAML.
        (Para custom queries creadas por usuario)
        """
        self._queries[query.name] = query
        self._save_to_file()
        return True
    
    def delete(self, name: str) -> bool:
        """Elimina una consulta."""
        if name in self._queries:
            del self._queries[name]
            self._save_to_file()
            return True
        return False
    
    def _save_to_file(self):
        """Guarda el diccionario de queries al YAML."""
        config = {
            'consultas': {
                name: query.to_dict()
                for name, query in self._queries.items()
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

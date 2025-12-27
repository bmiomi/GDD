from datetime import datetime
from typing import Dict, List
import yaml
import yaml_include

from .util import path,createfolder

class Config:
    """
    Clase base de configuración para todos los módulos.
    Proporciona acceso a config.yml y utilidades comunes.
    """

    __tiporevision:List=[]
    _cached_config = None
    
    @property
    def config(self) -> Dict:
        if self._cached_config is None:
            file = path.join("plugins", "xsales")
            # Registrar constructor !include para SafeLoader
            yaml.add_constructor("!include", yaml_include.Constructor(base_dir=file), Loader=yaml.SafeLoader)
            try:
                with open(f'{file}{path.sep}config.yml', 'r', encoding='utf-8') as f:
                    self._cached_config = yaml.load(f, Loader=yaml.SafeLoader)
            except FileNotFoundError as e:
                print(e, 'No se tiene archivo de configuracion.')
        return self._cached_config
    
    @property
    def fecha(self):
        return datetime.today().strftime("%Y-%m-%d")

    @property
    def path(self):
        return path
    
    @property
    def Turnos(self)-> List:
        return self.config['Turnos']

    @property
    def Revisiones(self) -> List:
        return self.__tiporevision

    @Revisiones.setter
    def Revisiones(self,value) -> List:
        self.__tiporevision=self.config['Revisiones'][value]

    def nuevacarpeta(self,*path):
        return createfolder(self.path,*path)
    
    def get_ftp_credentials(self, distribuidor: str) -> tuple[str, str]:
        """
        Obtiene credenciales FTP desde variables de entorno.
        
        Args:
            distribuidor: Nombre del distribuidor (PRONACA, CENACOP, etc.)
        
        Returns:
            Tupla (usuario, contraseña)
        """
        from core.config_manager import config_manager
        return config_manager.get_credential('FTP', distribuidor)

    def Dz(self, ldz: dict = {"Opcion": "TODOS"}) -> list[str]:
        """
        Retorna lista de distribuidores según la opción seleccionada.
        Intenta usar .env, si no existe hace fallback a config.yml
        """
        from core.config_manager import config_manager
        # Intentar obtener de .env primero
        try:
            todos_distribuidores = config_manager.list_available_distributors('FTP')
            if not todos_distribuidores:
                # Si no hay en .env, usar config.yml
                raise ValueError("No distributors in .env, using config.yml")
        except:
            # Fallback a config.yml (legacy)
            todos_distribuidores = list(self.config.get('datos', {}).get('FTP', {}).get('Repositorio', {}).get('credenciales', {}).keys())
        
        returndz = {
            "TODOS": todos_distribuidores,
            "Grupos": [self.config.get("Grupos", {})],
            "Maestros": self.config.get('datos', {}).get('FTP', {}).get('Maestros', {}).keys()
        }

        if ldz.get("Opcion") in ("REVICION_MADRUGADA", "Validar DESC"):
            v= [
                i
                for i in map(
                    lambda y: y.get(ldz["Turno"]), map(lambda x: x, returndz.get("Grupos")),
                )
                if i
            ][0]
            return v

        if ldz.get("Opcion") in ("Total_Pedidos","REVICION_MADRUGADA","Todas las rutas","VALIDAR_ClIENTE","DESC.DIURNOS","Descargar Base","TODOS"):
            return returndz.get("TODOS")

        if ldz.get("Opcion") == "Validar Maestros":
            return returndz.get("Maestros")
 
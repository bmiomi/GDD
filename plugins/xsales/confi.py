from datetime import datetime
from typing import Dict, List
from os import path
import yaml

from .util import sep,createfolder

def include_constructor(loader, node):
    """Constructor para manejar !include en archivos YAML"""
    try:
        include_file = loader.construct_scalar(node)
        
        # Obtener el directorio base del archivo principal
        if hasattr(loader, 'name') and loader.name:
            base_dir = path.dirname(loader.name)
        else:
            # Si no hay nombre, asumir que es relativo a plugins/xsales
            base_dir = path.join(path.dirname(__file__))
        
        file_path = path.join(base_dir, include_file)
        
        # Cargar y parsear el archivo incluido
        with open(file_path, 'r', encoding='utf-8') as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
            if content is None:
                return {}
            if not isinstance(content, dict):
                raise ValueError(f"The included file {file_path} does not contain a valid YAML dict, but {type(content)}")
            return content
    except Exception as e:
        raise

# Registrar el constructor personalizado
yaml.add_constructor('!include', include_constructor, yaml.FullLoader)

class Config:

    __tiporevision:List=[]

    @property
    def config(self) -> Dict:
        file = path.join(f"plugins{sep}xsales{sep}config.yml")
        try:
            with open(file, "r", encoding='utf-8') as f:
                loader = yaml.FullLoader(f)
                loader.name = file  # Guardar el nombre del archivo para referencia
                return loader.get_single_data()
        except FileNotFoundError :
           raise FileExistsError("No se tiene archivo de configuracion.")

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
        self.__tiporevision=self.config['Revisiones'][value.get('Modulo')]

    def nuevacarpeta(self,*path):
        return createfolder(self.path,*path)

    def Dz(self, ldz: dict = {"Opcion": "TODOS"}) -> list[str]:

        returndz = {

            "TODOS": self.config["datos"]["FTP"]["Repositorio"]["credenciales"].keys(),
            "Grupos": [self.config["Grupos"]],
            "Maestros":self.config['datos']['FTP']['Maestros'].keys()
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

        if ldz.get("Opcion") == "Total_Pedidos":
            return returndz.get("TODOS")

        if ldz.get("Opcion") == "REVICION_MADRUGADA":
            return returndz.get("TODOS")
        
        # Retorno por defecto
        return list(returndz.get("TODOS", []))


    

from datetime import datetime
from typing import Any, Dict, List
from os import path
import yaml
from .util import sep, createfolder


def include_constructor(loader, node):
    """Constructor para manejar !include en archivos YAML."""
    include_file = loader.construct_scalar(node)

    if hasattr(loader, 'name') and loader.name:
        base_dir = path.dirname(loader.name)
    else:
        base_dir = path.join(path.dirname(__file__), '..')

    file_path = path.join(base_dir, include_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        if content is None:
            return {}
        if not isinstance(content, dict):
            raise ValueError(
                f"The included file {file_path} does not contain a valid YAML dict, "
                f"but {type(content)}"
            )
        return content


yaml.add_constructor('!include', include_constructor, yaml.FullLoader)

class Config:

    __tiporevision:List=[]

    @property
    def config(self) -> Dict:
        file = path.join(f"plugins{sep}xsales{sep}config.yml")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                loader = yaml.FullLoader(f)
                loader.name = file
                return loader.get_single_data()
        except FileNotFoundError:
            print("No se tiene archivo de configuracion.")
            exit()

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
        # Aceptar tanto dict con clave 'Modulo' como string directo
        if isinstance(value, dict):
            modulo = value.get('Modulo')
        elif isinstance(value, str):
            modulo = value
        else:
            raise TypeError("Revisiones debe ser dict con 'Modulo' o string del nombre de módulo")

        if modulo not in self.config['Revisiones']:
            raise KeyError(f"Modulo de revisión desconocido: {modulo}")

        self.__tiporevision = self.config['Revisiones'][modulo]

    def nuevacarpeta(self, *path):
        return createfolder(*path)

    def Dz(self, ldz: dict = {"Opcion": "TODOS"}) -> list[str]:
        datos = self.config.get("datos", {})
        ftp = datos.get("FTP", {})
        repo = ftp.get("Repositorio", {})
        credenciales = repo.get("credenciales", {})
        grupos = self.config.get("Grupos") or {}

        returndz = {
            "TODOS": credenciales.keys(),
            "Grupos": [grupos]
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
            return list(returndz.get("TODOS") or [])

        if ldz.get("Opcion") != "REVICION_MADRUGADA":
            return list(returndz.get("TODOS") or [])

 

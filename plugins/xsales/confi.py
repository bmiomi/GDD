from datetime import datetime
from logging import config
from typing import Dict, List, Self
from os import path
import yaml
from yamlinclude import YamlIncludeConstructor 
from .util import sep,createfolder

class Config:

    __tiporevision:List=[]
    _cached_config = None
    
    @property
    def config(self) -> Dict:
        if self._cached_config is None:
            file = path.join("plugins", "xsales")
            YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=file)
            try:
                self._cached_config = yaml.load(open(f'{file}\config.yml'), Loader=yaml.FullLoader)
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

    def Dz(self, ldz: dict = {"Opcion": "TODOS"}) -> list[str]:
        returndz = {

            "TODOS": self.config['datos']["FTP"]["Repositorio"]["credenciales"].keys(),
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

        if ldz.get("Opcion") in ("Total_Pedidos","REVICION_MADRUGADA","Todas las rutas","VALIDAR_ClIENTE","DESC.DIURNOS","Descargar Base","TODOS"):
            return returndz.get("TODOS")

        if ldz.get("Opcion") == "Validar Maestros":
            return returndz.get("Maestros")
 



    

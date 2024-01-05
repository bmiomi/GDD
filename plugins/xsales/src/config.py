from datetime import datetime
from typing import Any, Dict, List
import yaml
from .util import  path,sep,createfolder

class Config:

    __tiporevision:List=[]

    @property
    def config(self) -> Dict:
        file = path.join(f"plugins{sep}xsales{sep}config.yaml")
        try:
            return yaml.load(open(file, "r"), Loader=yaml.FullLoader)
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
        self.__tiporevision=self.config['Revisiones'][value.get('Modulo')]

    def nuevacarpeta(self, *path):
        return createfolder(*path)

    def Dz(self, ldz: dict = {"Opcion": "TODOS"}) -> list[str]:
        returndz = {
            "TODOS": self.config["FTP"]["Repositorio"]["credenciales"].keys(),
            "Grupos": [self.config["Grupos"]]
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

        if ldz.get("Opcion") != "REVICION_MADRUGADA":
            return returndz.get("TODOS")

 

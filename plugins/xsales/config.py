from datetime import datetime
from io import StringIO
from typing import Dict, List
import pandas as pd
import yaml

from .util import  path, remove, listdir,sep,createfolder

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



    

class ExcelFile:

    """
    Clase  en donde  se procesan y generan archivos de Excel

    """

    _nombrearchivo = f"reporte{ Config().fecha}.xlsx"

    @classmethod
    def excelfile(cls):
        """

        si el archivo exite  validar que la fecha sea igual a la actual.
        si el archivo no exite crear un archivo

        """

        d = datetime.today().date().strftime("%d/%m/%Y")
        c = datetime.fromtimestamp(path.getmtime(cls._nombrearchivo)).strftime(
            "%d/%m/%Y"
        )

        if c != d:
            print("\n removiendo el archivo")
            remove(cls._nombrearchivo)

    @classmethod
    def recorrer_tabla(
        cls, data: str, converts={"Codigo_Cliente": str, "Id_Negociacion": str}
    ) -> pd.DataFrame:
        return pd.DataFrame(
            pd.read_html(StringIO(data), converters=converts)[0]
        ).to_dict("records")

    @classmethod
    def append_df_to_excel(cls, dfs):
        df = pd.DataFrame(dfs)
        if not path.isfile(cls._nombrearchivo):
            df.to_excel(cls._nombrearchivo, index=False)
        else:
            df_excel = pd.read_excel(cls._nombrearchivo, dtype="str")
            result = pd.concat([df_excel, df], ignore_index=True)
            result.to_excel(cls._nombrearchivo, index=False, sheet_name="GDD")

    @classmethod
    def consolidararchivo(cls):
        pathexcel = path.join(ConfigServer().folderexcel())
        r = listdir(pathexcel)
        t = path.abspath(pathexcel)
        for i in range(len(r)):
            directorio = t + "\\" + r[i]
            q = pd.read_excel(directorio, dtype="str")
            cls.append_df_to_excel(q)

    @classmethod
    def filetxt(cls, namearchivo: str, data: dict):
        archiv = "".join([namearchivo, Config().fecha])
        with open(archiv, "a") as file:
            for key, value in data.items():
                file.writelines(f"{key} - {value}\n")


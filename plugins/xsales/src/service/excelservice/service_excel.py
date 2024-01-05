import datetime
from typing import Any, Hashable
import pandas as pd
from io import StringIO

from plugins.xsales.confi import Config
from ....util import  remove, listdir


class ExcelFile:

    Cdf=pd.DataFrame()

    """
    Clase  en donde  se procesan y generan archivos de Excel

    """

    _nombrearchivo = f"reporte{ Config().fecha}.xlsx"


    config:Config=Config()


    @classmethod
    def excelfile(cls):
        """
        valida si un archivo excel ya existe en caso de existir procede a elimarlo

        si el archivo exite  validar que la fecha sea igual a la actual.
        si el archivo no exite crear un archivo

        """
        try:

            d = datetime.datetime.today().date().strftime("%d/%m/%Y")
            c = datetime.datetime.  fromtimestamp(cls.config.path.getmtime(cls._nombrearchivo)).strftime("%d/%m/%Y")

            if c != d:
                remove(cls._nombrearchivo)
                return "\n removiendo el archivo"
        except FileNotFoundError as e:
                return f'no se encontro archivo {cls._nombrearchivo} a eliminar'


    @classmethod
    def recorrer_tabla(
        cls, 
        data: str,
        converts={"Codigo_Cliente": str, "Id_Negociacion": str}
    ) -> list[dict[Hashable, Any]]:
        "procede a leer el archivo html y convertilo, en un diccionario de datos estructurados"
        return pd.DataFrame(
            pd.read_html(StringIO(data), converters=converts)[0]
        ).to_dict("records")


    @classmethod
    def append_df_to_excel(cls, nombre,dfs,config):

        # nombrearchivo=config.path.join(nombre,config.fecha+'.xlsm')
        temporal=pd.DataFrame(dfs)
        cls.Cdf=pd.concat([temporal,cls.Cdf])

        # result.to_excel(config.folderexcel+nombrearchivo, index=False, sheet_name=nombre)


    @classmethod
    def consolidararchivo(cls, config):
        pathexcel = config.path.join(config.folderexcel) 
        r = listdir(pathexcel)

        t = config.path.abspath(pathexcel)
        for i in range(len(r)):
            directorio = t + "\\" + r[i]
            q = pd.read_excel(directorio, dtype="str")
            cls.append_df_to_excel(q)


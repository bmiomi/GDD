import datetime
import pandas as pd
from io import StringIO
from plugins.xsales.confi import Config
from ....util import  remove, listdir


class ExcelFile:

    """
    Clase  en donde  se procesan y generan archivos de Excel

    """

    _nombrearchivo = f"reporte{ Config().fecha}.xlsx"

    config:Config


    @classmethod
    def excelfile(cls):
        """

        si el archivo exite  validar que la fecha sea igual a la actual.
        si el archivo no exite crear un archivo

        """

        d = datetime.today().date().strftime("%d/%m/%Y")
        c = datetime.fromtimestamp(cls.config.path.getmtime(cls._nombrearchivo)).strftime(
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


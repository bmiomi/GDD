import os
import pandas as pd
from ....util import  remove, listdir


class ExcelFile:

    Cdf=None
    """
    Clase  en donde  se procesan y generan archivos de Excel

    """

    @classmethod
    def validarexcel(cls,directorio):

        archivos = listdir(directorio)
        archivos_excel = [archivo for archivo in archivos if archivo.endswith('.xlsx')]
        if len(archivos_excel) > 0:
            numeros = [archivo.split('.')[0] for archivo in archivos_excel]
            return max(numeros)
        else:
            return 0

    @classmethod
    def read_list_files(cls, directorio):
        for file in directorio:
            dfs = pd.read_excel(file, dtype="str")
            cls.Cdf=pd.concat([dfs,cls.Cdf],ignore_index=True)

    @classmethod
    def create_file(cls,archivo,data):

        dfs=[ pd.DataFrame(df) for df in data]
        cls.Cdf=pd.concat(dfs,ignore_index=True)
        # narchivos=cls.validarexcel(paths)
        # archivo=os.path.join(paths,f"{ narchivos if narchivos!=0 else None}.xlsx")
        cls.Cdf.to_excel(f'{archivo}.xlsx',index=False)
        cls.Cdf.to_string(f'{archivo}.txt',index=False)
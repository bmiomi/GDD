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

    @classmethod
    def create_file_by_sheets(cls, archivo, datos_por_turno: dict):
        """
        Crea un Excel con múltiples hojas (una por turno).
        
        Args:
            archivo: Ruta base del archivo (sin extensión)
            datos_por_turno: Dict {turno: [lista de dicts con datos]}
        """
        file_path = f'{archivo}.xlsx'
        file_exists = os.path.exists(file_path)

        # Si existe, actualiza/reescribe solo la hoja del turno
        writer_kwargs = {
            "engine": "openpyxl",
            "mode": "a" if file_exists else "w",
            "if_sheet_exists": "replace" if file_exists else None,
        }
        if writer_kwargs["if_sheet_exists"] is None:
            writer_kwargs.pop("if_sheet_exists")

        with pd.ExcelWriter(file_path, **writer_kwargs) as writer:
            for turno, datos in datos_por_turno.items():
                if datos:
                    df = pd.DataFrame(datos)
                    # Normalizar nombre de hoja (max 31 caracteres, sin caracteres especiales)
                    sheet_name = str(turno)[:31].replace('/', '-').replace('\\', '-').replace('*', '').replace('[', '').replace(']', '').replace(':', '-').replace('?', '')
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # También guardar TXT consolidado
        all_data = []
        for datos in datos_por_turno.values():
            all_data.extend(datos)
        if all_data:
            df_all = pd.DataFrame(all_data)
            df_all.to_string(f'{archivo}.txt', index=False)
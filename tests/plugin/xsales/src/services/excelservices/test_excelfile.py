from plugins.xsales.src.modules.Server import Page
from plugins.xsales.src.modules.Server.Pagedriver.xsalesbeta import Xsales
from plugins.xsales.src.modules.Server.User import Consultas
from plugins.xsales.src.modules.Server.config import ConfigServer
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile

from unittest import TestCase,main
import json
import pandas as pd

def cargardatos():
    datos= open('tests\\data\\Reporte_Pedidos.json') 
    return json.load(datos)

class Test_Excelfile(TestCase):

    def setUp(self) -> None:
        self.test_EFile=ExcelFile

    def test_excelfile(self):
        value=self.test_EFile.excelfile()
        self.assertEqual(value,'no se encontro archivo reporte2023-12-18.xlsx a eliminar')

    def test_agregar_datos(self):

        xsales=Xsales('PRONACA')
        sql=Consultas.consultas.Descuentos_Demadrugada("PRONACA")
        result=xsales.consulta_new_version(sql=sql)        
        df=self.test_EFile.recorrer_tabla(result)
        self.test_EFile.create_file()

        self.assertIsInstance(df,pd.DataFrame)

    def test_create_file(self):
        self.test_EFile.create_file('Revision_Matutina',cargardatos(),ConfigServer())
        
if __name__=="__main__":
    main()
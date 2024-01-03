
from plugins.xsales.src.modules.Server.config import ConfigServer
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile

from unittest import TestCase,main
import json

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
       for _ in range(3):
           self.test_EFile.append_df_to_excel('PEDIDO_',cargardatos(),ConfigServer())

if __name__=="__main__":
    main()
from unittest import TestCase,main
from plugins.xsales.src.modules.Server.config import ConfigServer
import json


class Tests_ConfigServer(TestCase):

    def setUp(self) -> None:
        self.testconfig=ConfigServer()
        with open('.\\tests\\data\\Consultas.json') as json_File:
            self.json=json.load(json_File)

    def test_credenciales(self):
        print(f"respuesta: {self.testconfig.configserver['credenciales'][0]['default']}")
        self.assertIsNotNone(self.testconfig.CredencialesServer)


    def test_foldermadrugada(self):
        self.testconfig.Revisiones
        self.assertEqual(type(self.testconfig.folderMadrugada),str)


    def test_consultas(self):
        self.assertEqual(type(self.testconfig.configserver['Consultas']), dict)

    def test_string_REVICION_MADRUGADA(self):
            stringyalm = self.testconfig.configserver['Consultas']['REVICION_MADRUGADA']['sql']['then'].replace('\\', ' ').replace('\n', ' ').replace('\t', ' ').replace(' ','')
            stringjson="".join(self.json['REVICION_MADRUGADA']['sql']['PRONACA'] ).replace(" ", "")
            self.assertEqual( stringyalm, stringjson)

    def test_validar_Variables(self):   
        
        self.testconfig.configserver['Consultas']['REVICION_MADRUGADA']['parametros'][1] = {'NDISTRIBUIDOR': 'PRONACA'}
        NDISTRIBUIDOR = self.testconfig.configserver['Consultas']['REVICION_MADRUGADA']['parametros'][1]['NDISTRIBUIDOR']

        if NDISTRIBUIDOR == "PRONACA":
            consulta_sql = self.testconfig.configserver['Consultas']['REVICION_MADRUGADA']['sql']['then']
        else:
            # Ejecuta la consulta SQL correspondiente
            consulta_sql = self.testconfig.configserver['Consultas']['REVICION_MADRUGADA']['sql']['else']

        # # Ahora, podemos utilizar la variable NDISTRIBUIDOR en el archivo YAML
        # yaml_config = self.testconfig.configserver['Consultas']['REVICION_MADRUGADA']
        # yaml_config['sql']['if'] = f"{{NDISTRIBUIDOR}} == 'ALSODI'"
        # print(yaml_config['sql']['if'])

        self.assertEqual(consulta_sql.replace(" ", ""),self.json['REVICION_MADRUGADA']['sql']['PRONACA'].replace(" ", ""))




if __name__=="__main__":
    main()
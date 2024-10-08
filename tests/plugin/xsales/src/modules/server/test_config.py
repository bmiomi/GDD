from unittest import TestCase,main

from plugins.xsales.src.modules.Server.config import ConfigServer


class Tests_ConfigServer(TestCase):

    def setUp(self) -> None:
        self.testconfig=ConfigServer()

    def test_credenciales(self):
        print(f"respuesta: {self.testconfig.configserver['credenciales'][0]['default']}")
        self.assertIsNotNone(self.testconfig.CredencialesServer)


    def test_foldermadrugada(self):
        self.testconfig.Revisiones
        self.assertEqual(type(self.testconfig.folderMadrugada),str)

    def test_Consultas(self):
      self.assertEqual( type(sef.testconfig['Consultas']),dict)


if __name__=="__main__":
    main()
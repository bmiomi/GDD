from unittest import TestCase,main
from plugins.xsales.src.modules.Server.config import ConfigServer

class Tests_Config(TestCase):

    def setUp(self) -> None:
        self.testconfig=ConfigServer()

    def test_credenciales(self):
        self.testconfig.CredencialesServer='default'
        print(f"respuesta: {self.testconfig.CredencialesServer}")
        self.assertIsNotNone(self.testconfig.CredencialesServer)


    def test_foldermadrugada(self):
        print(self.testconfig.folderMadrugada)
        self.assertEqual(type(self.testconfig.folderMadrugada),str)

if __name__=="__main__":
    main()
from unittest import TestCase, main
from plugins.xsales.confi import Config
from datetime import date

class TestConfig(TestCase):
    
    def setUp(self) -> None:
        self.config=Config()

    def test_config(self):
        self.assertEqual( type(self.config.config ),dict)  

    def test_fecha(self)->date:
        pass

    def test_path(self):
        print(f'mi Molulo: {self.config.path}')

    def test_file_ftp(self):
        self.config.config['datos'],{'dato':'hola mundo'}

    def test_file_server(self):
        self.config.config['datod'],{'config':'asd'}


    def test_Dz(self):
        pass










if __name__=="__main__":
    main()



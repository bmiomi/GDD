from unittest import TestCase,main
from plugins.xsales.src.modules.Server.User.Consultas import consultas
from plugins.xsales.src.modules.Server.config import ConfigServer

class Test_Consultas(TestCase):

    def setUp(self) -> None:
       self.config=ConfigServer()


    def test_obtener_query(self):
       result= consultas.consulta_beta( 'Consultas',
                                        'DESC.NOCTURNOS',
                                        self.config.configserver
                                        )
#       self.assertIsInstance(result ,dict)
       self.assertEqual(" {{PRONACA}} == 'PRONACA' ",result)




if __name__=="__main__":
  main()
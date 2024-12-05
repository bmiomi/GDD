from unittest import TestCase,main

from plugins.xsales.src.modules.Server import Page


class Tests_Page(TestCase):

    def setUp(self) -> None:
        self.page=Page()

    def test_instancia(self):
        self.assertIsInstance(self.page,Page)
    
    def test_opcion(self):
        self.page.name='Cenacop'
        self.page.get_consulta('Total_Pedidos') 


if __name__=='__main__':
    main()
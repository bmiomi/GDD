from unittest import TestCase
 
from plugins.xsales.src.modules.Status import Status

class Test_Status(TestCase):

    def setUp(self) -> None:
        self.tstatus=Status()

    def test_datos(self):   

        self.tstatus.dato={}

        self.assertEquals(type(self.tstatus.dato),dict)


    def test_listardz(self):

        # dzs=self.tstatus.config.Dz()
        self.assertEquals(len(self.tstatus.dz),24)

    def test_restardz(self):
        pass
    
    def test_statusrutas(self):

        statusdz=self.tstatus.statusrutas('Paul_florencia')

        print(statusdz)
<<<<<<< HEAD
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
=======
from unittest import TestCase,main

from plugins.xsales.src.modules.Status.Status import Status

class Test_Status(TestCase):
    
    def setUp(self) -> None:
        self.teststatus=Status()

    def test_dz(self):
       print(self.teststatus.dz)
       self.assertEqual(type(self.teststatus.dz),list)

    def test_retornardz(self):

        with self.assertRaises(ValueError) as cm:
            redz=self.teststatus.retornardz('CENACOP')
        self.assertEqual(str(cm.exception), "No existen DZ que validar")
  
    def test_dzcompletar(self):
        self.assertEqual(len(self.teststatus.dzincompletos),23)

    def test_statusrutas_error(self):

        with self.assertRaises(BaseException) as cm:
            self.teststatus.statusrutas('as')
        self.assertEqual(str(cm.exception), "Direccion no valida")

    def test_statusrutas_ok(self):
        r=self.teststatus.statusrutas('Disanahisa')
        self.assertEqual(type(r),tuple)



if __name__=='__main__':
    main()



dz=22
dzcompletos=1
>>>>>>> 6809dd0e76ee732e8887cd9e0e71a1ea12626e95

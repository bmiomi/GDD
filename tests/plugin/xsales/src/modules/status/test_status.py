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

    def test_statusrutas(self):

        with self.assertRaises(BaseException) as cm:
            self.teststatus.statusrutas('as')
        self.assertEqual(str(cm.exception), "Direccion no valida")

            
if __name__=='__main__':
    main()




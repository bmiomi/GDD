from unittest import TestCase,main
from plugins.xsales.src.modules.Status.Status import Status

class Test_Status(TestCase):
    
    def setUp(self) -> None:
        self.teststatus=Status()

    def test_dz(self):
       print(self.teststatus.dzcompletos)
       self.assertEqual(type(self.teststatus.dzincompletos),list)

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


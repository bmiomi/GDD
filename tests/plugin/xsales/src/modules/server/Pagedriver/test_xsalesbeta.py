import unittest

from plugins.xsales.src.modules.Server.Pagedriver.xsalesbeta import Xsales


class test_xsalesbeta(unittest.TestCase):


    DZS= ['ALSODI', 'ALMABI', 'DIMMIA', 'DISANAHISA', 'DISPROALZA', 'DISPROVALLES', 'DISMAG', 'GARVELPRODUCT', 'JUDISPRO', 'MADELI', 'PAUL_FLORENCIA', 'APRONAM', 'DISCARNICOS', 'PRONACNOR', 'GRAMPIR', 'CENACOP', 'POSSO_CUEVA', 'ECOAL', 'SKANDINAR', 'APRONAM', 'PATRICIO_CEVALLOS', 'H_M', 'DAPROMACH', 'PROORIENTE']

    def setUp(self) -> None:
        self.xsales=Xsales('PRONACA')

    def tearDown(self) -> None:
        del self.xsales

    def test_login(self):
       self.assertEqual(self.xsales.responsexsales.status_code,200)

    def test_respuestaxsales(self):
        self.xsales.HEADERS       
        res=self.xsales.consulta_new_version('select top 100 * from demand')
        print(res,file=open('asd.txt','w'))

    def test_version_xsales(self):
        anterior=[]    
        for name in self.DZS:
            self.xsale=Xsales(name)
            vale=self.xsale.versionxsales()
            if vale != "XSales® SFA - 4.4.1 AFG":
                anterior.append(f"{name}-{vale}")
        self.assertIsInstance(list(anterior),list)

    def test_logins(self):
        self.xsales.logerarseesion()

    def test_cantidadnuevaversion(self):

        estado=False
        newversion=[]
        olvversion=[]
        while estado is not True:
            for i in[ "ALSODI", "ALMABI", "DIMMIA", "DISANAHISA", "DISPROALZA", "DISPROVALLES", "DISMAG", "GARVELPRODUCT", "PRONAIM", "JUDISPRO", "MADELI", "PAUL_FLORENCIA", "APRONAM", "DISCARNICOS", "PRONACNOR", "GRAMPIR", "CENACOP", "POSSO_CUEVA", "ECOAL", "SKANDINAR", "APRONAM", "PATRICIO_CEVALLOS", "H_M", "DAPROMACH", "PROORIENTE"]:
                dz= Xsales(i)
                version=dz.versionxsales()
                if version == 'XSales® SFA - 4.4.1 AFG':
                    newversion.append(i)
                else:
                    olvversion.append(i)
            estado=False
        self.assertEqual(type(newversion),list)

    def test_consultar(self):
       self.assertIsInstance( self.xsales.consulta_new_version('Select top 1000 * from customer'),str)

if __name__=="__main__":
    unittest.main()
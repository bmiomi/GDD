import unittest

from plugins.xsales.src.modules.FTP import FtpXsales


class Test_Ftp(unittest.TestCase):


    def setUp(self) -> None:
        self.ftp=FtpXsales()

    def test_prueba(self):
        self.ftp.procesarInfo('REPORTES\\FTP\\Distribuidores\\DISPROLOP\\2024-05-18\\250')



if __name__=="__main::":
    unittest.main()
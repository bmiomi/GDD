<<<<<<< HEAD
# -*- coding: utf-8 -*-
from .FTP import FtpXsales
from .Status.Status import Status 
from .Server import Page

class XsalesFactory:

    @classmethod
    def getModulo (cls,value:str) -> object:
        modulo={'Server':Page,'Ftp':FtpXsales,'Status':Status}
        return modulo.get(value)()



=======
# -*- coding: utf-8 -*-
from .Ftp import FtpXsales
from .Status.Status import Status 
from .Server import Page

class XsalesFactory:

    @classmethod
    def getModulo (cls,value:str) -> object:
        modulo={'Server':Page,'Ftp':FtpXsales,'Status':Status}
        return modulo.get(value)()



>>>>>>> 8be410330e0e34aa49b9dec88801aabcfc683771

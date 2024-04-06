# -*- coding: utf-8 -*-
from typing import  Dict
from .Ftp import FtpXsales
from .Status.Status import Status 
from .Server import Page

class XsalesFactory:

    @classmethod
    def getModulo (cls,value:str) -> object:
        modulo={'Server':Page(),'FTP':FtpXsales(),'Status':Status()}
        return modulo.get(value)




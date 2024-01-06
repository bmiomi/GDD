# -*- coding: utf-8 -*-
from typing import  Dict
from .FTP import FtpXsales
from .Status.Status import Status 
from .Server import Page

class XsalesFactory:
    
    @classmethod
    def getModulo (cls,value:Dict=None) -> object:
        modulo={'Server':Page(),'FTP':FtpXsales(),'Status':Status()}
        return modulo.get(value['Modulo'])

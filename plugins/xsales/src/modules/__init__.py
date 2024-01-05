# -*- coding: utf-8 -*-
from typing import  Dict
from .FTP import FtpXsales
from .Status.Status import Status 
from .Server import Page

class XsalesFactory:
    
    @classmethod
<<<<<<< HEAD
    def getModulo (cls,value:Dict=None) -> object:
        modulo={'Server':Page,'FTP':FtpXsales,'Status':Status}
        return modulo.get(value['Modulo'])
=======
    def getModulo (cls,value:Dict=None)-> object:
        
        modulo=value.get('Modulo')
        
        if modulo == 'Server':
            return Page()
        if modulo == 'FTP':
            return FtpXsales()
        if  modulo== 'Status':
            return Status()
>>>>>>> 6809dd0e76ee732e8887cd9e0e71a1ea12626e95

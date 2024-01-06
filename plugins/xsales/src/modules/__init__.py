# -*- coding: utf-8 -*-
from typing import  Dict
from .FTP import FtpXsales
from .Status.Status import Status 
from .Server import Page

class XsalesFactory:
    
    @classmethod
<<<<<<< HEAD
    def getModulo (cls,value:Dict=None)-> object:
        
        modulo=value.get('Modulo')
        
        if modulo == 'Server':
            return Page()
        if modulo == 'FTP':
            return FtpXsales()
        if  modulo== 'Status':
            return Status()
=======
    def getModulo (cls,value:Dict=None) -> object:
        modulo={'Server':Page(),'FTP':FtpXsales(),'Status':Status()}
        return modulo.get(value['Modulo'])
>>>>>>> de0a5f2993584932b82597354112f11d68d3414d

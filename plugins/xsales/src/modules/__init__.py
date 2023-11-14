# -*- coding: utf-8 -*-
from typing import Dict
from .FTP import FtpXsales
from .Status import Status 
from .Server import Page

class XsalesFactory:
    
    __factory={"Server":Page(),'FTP':FtpXsales(),"Status":Status()}
    
    @classmethod
    def getModulo (cls,value:Dict=None) -> object:
        return XsalesFactory.__factory.get(value.get('Modulo'))        

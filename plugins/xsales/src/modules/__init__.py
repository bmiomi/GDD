# -*- coding: utf-8 -*-
from typing import Dict
from .FTP import FtpXsales
from .Status import Status 
from .Server import Page

class XsalesFactory:
    
    @classmethod
    def getModulo (cls,value:Dict=None) -> object:
        
        modulo=value.get('Modulo')
        
        if modulo == 'Server':
            return Page
        if modulo == 'FTP':
            return FtpXsales
        if  modulo== 'Status':
            return Status

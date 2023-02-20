# -*- coding: utf-8 -*-
from .FTP import FtpXsales
from .Status import Status 
from .Server import Page

class XsalesFactory:
    
    @classmethod
    def getModulo (cls,value:str=None) -> object:
        if value == 'Server':
            return Page
        if value == 'FTP':
            return FtpXsales
        if  value== 'Status':
            return Status

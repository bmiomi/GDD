from typing import Dict
from plugins.xsales.config import Config,ConfigServer,ExcelFile
from plugins.xsales.Xsales import XsalesFactory 

def test_config():
    # config:Config=Config()
    
    # c=config.config['Consultas']['server']['CLIENTES']
    
    server=XsalesFactory.getModulo('Server')
    s=server('Cenacop',ConfigServer()) 
    s.consulta_Basedatos( 'CLIENTES',ExcelFile)

    print(s)

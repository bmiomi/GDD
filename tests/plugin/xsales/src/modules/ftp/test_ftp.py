# from questionary import prompt
# from rich.console import Console

# from plugins.xsales.src.modules.FTP import FtpXsales
# from plugins.xsales.confi import ConfigFactory
# from plugins.xsales.Xsales import Data



# def test_prueba():
#     console=Console()

#     ftp=ConfigFactory.getModulo('FTP')

#     data={'ContenedorDZ':['Xsales'],'Turno':'TECNICO 3.a.m','questionary':prompt,'console':console,'Opcion':'Validar Maestros'}

#     result=Data(**data)

#     ftp=FtpXsales(result,ftp)
#     ftp.maestrosftp()

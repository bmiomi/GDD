from MODULOS.Vista.Interface_CLI.VistaCLI import main
from MODULOS.Modelo.FtpXsales import FtpXsales


if __name__ == '__main__':
    try:
        if input('DESEA EJECUTAR EL SERVIDOR-WEB: ') in ('Si','si','s','S'):
            from MODULOS.Vista.Interface_Web.index import app
            app.run() 
        else:
            main()    
    except KeyboardInterrupt as identifier:
        print('has Cerrado de una manera forsosa el programa')
        exit()


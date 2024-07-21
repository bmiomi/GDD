from typing import List

import questionary

from plugins.xsales.src.modules.Ftp.enums.enumftp import Enumftp
from plugins.xsales.util import descomprimir,sep,path
from ...service.dbservice.sqliteservices import DataConn
from .ftp import ImplicitFTPTLS
from .interface.IFtp import IFtp
from .sftp import SFTP_
from .config import ConfigFtp

linea = '-' * 60
class FtpXsales:

    """Conexion con el Ftp de Xsales"""

    config=ConfigFtp()

    def __init__(self) -> None:
        self.config.Revisiones='Ftp'
        self.dato=None
        self.__ftp_client:IFtp = ImplicitFTPTLS() if self.config.protocol== 'FTPS' else  SFTP_()
        self.rutascero = []

    def listbases(self) -> List[str]:
        dirs = []
        self.__ftp_client.change_dir(self.config.pathdownload)
        self.__ftp_client.list_dir(lambda x: dirs.extend(x.splitlines()))
        return [filename[49:] for filename in dirs if not filename[49:].startswith('T')and filename[49:] not in self.config.excluide]

    def procesar_base(self,destinopath:str)->None:
##TODO
        # VALORES A ARREGLAR
        origenpath= ''.join([i for i in destinopath.rsplit(sep)[-1] ])
        database = destinopath+sep+"Main.sqlite"
        with  open(f"{destinopath[:-len(origenpath)]}{sep}log.txt", 'a') as archivo, DataConn(database) as conn:
            archivo.write(linea+'\n')
            archivo.write("Ruta: "+origenpath+'\n')
            for table in self.config.tablevalidacion:
                result = conn.execute(f"SELECT COUNT(*) FROM  {table} WHERE DISCODE NOT LIKE 'DES%'")
                result, =result.fetchone()
                archivo.write(f"REGISTROS EN {table}: {result}\n")
                if result == 0:
                    self.rutascero.append({'ruta':origenpath,'table':table,'result':result})

                # if len(self.rutascero)>3:
                #     print(self.rutascero)
                #     raise ValueError ("Rutas con modulos Bloqueado")

    def maestrosftp(self):
        self.__ftp_client.mostrarar_achivos(excluide=self.config.xmlfile)

    def mostrar_info(self,dz,console):
        self.config.operacion=self.dato.Opcion
        self.config.user=dz[0]
        self.__ftp_client.acceso( self.config.host, *self.config.CredencialesFtp)
        if self.dato.Opcion==Enumftp.Validar_Maestros.value:
            self.maestrosftp()
            console.log(self.__ftp_client.files)
        if self.dato.Opcion==Enumftp.Validar_DESC.value:
            _rutas:list[str] = self.listbases()
            lista_rutas=questionary.checkbox("Seleccione las bases a descargar",choices= _rutas).ask()
       
            with  console.status('Procesando',spinner=self.config.spinner):

                try:
                    self.procesar_info(lista_rutas,console)
                except ValueError as e:
                    console.print(" [ERROR: ][bold red] No se tiene Habilitado Modulo de GDD [\]", e)
                except BaseException as e:
                    print( 'se tiene error: ',e)

    #2022 09 15 03 45 02
    def procesar_info(self,lista_rutas,console):
        if len(lista_rutas)>=1:
            for i in lista_rutas:
                path=self.config.nuevacarpeta(
                                              self.config.pathdistribudor,
                                              self.config.user,
                                              self.config.fecha,
                                              i
                                              )
                self.__ftp_client.descarga(i,path,self.config.downloadfilebaseruta)
                descomprimir(path)
                currentpath=path.join([path])
                self.procesar_base(currentpath)
                console.log(f' proceso exitoso,validar archivo: {path[:-3]}{sep}log')
        else:
            console.print(" [ERROR: ][bold red] NO SE TINE RUTAS QUE ITERAR")

    def generararchivo(self,r,t,w):
        pass
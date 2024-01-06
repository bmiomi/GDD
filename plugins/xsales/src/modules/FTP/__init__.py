from typing import List

from plugins.xsales.util import descomprimir,sep
from ...service.dbservice.sqliteservices import DataConn
from .ftp import ImplicitFTPTLS
from .IFtp import IFtp
from .sftp import SFTP_
from .config import ConfigFtp


linea = '-' * 60

class FtpXsales:

    """

        Conexion con el Ftp de Xsales

    """
    config=ConfigFtp()

    def __init__(self) -> None:
        self.dato=None
        # self.config.operacion=self.dato.Opcion
        self.rutascero = []

    def listbases(self) -> List[str]:
        dirs = []
        self.__ftp_client.change_dir(self.config.pathdownload)
        self.__ftp_client.list_dir(dirs.append)
        return [filename[49:] for filename in dirs
        if not filename[49:].startswith('T')
        and filename[49:] not in self.config.excluide
        ]

    def DESCARGA(self,origenpath,destinopath)->None:
        self.__ftp_client.change_dir(origenpath)
        with open(f"{destinopath}{sep}Main.zip", 'wb') as file:
            self.__ftp_client.retrbinary('RETR '+'Main.zip', file.write)
        self.__ftp_client.change_dir('..')

    def procesarInfo(self,destinopath:str)->None:

        origenpath= ''.join([i for i in destinopath.rsplit(sep)[-1] ])
        database = destinopath+sep+"Main.sqlite"
        tablas=['DISCOUNTDETAIL','DISCOUNTROUTE']

        with  open(f"{destinopath[:-len(origenpath)]}{sep}logo", 'a') as archivo, DataConn(database) as conn:
            archivo.write(linea+'\n')
            archivo.write("Ruta: "+origenpath+'\n')

            for table in tablas:
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
       
       with  console.status('Procesando',spinner=self.config.spinner):
            self.config.operacion=self.dato.Opcion

            self.config.user=dz[0]
            self.__ftp_client:IFtp =  ImplicitFTPTLS() if self.config.protocol== 'FTPS' else  SFTP_()
            self.__ftp_client.acceso(
                self.config.host,
                *self.config.CredencialesFtp
                )

            if self.dato.Opcion=='Validar Maestros':
                self.maestrosftp()
                console.log(self.__ftp_client.file)
            else:
                _rutas = self.listbases()
                try:
                    # self.dato.console.print(f'Para {dz} se descargara {len(_rutas)} rutas')
                    if len(_rutas)>=1:
                        for i in _rutas:
                            path=self.config.nuevacarpeta(self.config.pathdistribudor,self.config.user,self.config.fecha,i)
                            self.DESCARGA(i,path)
                            descomprimir(path)
                            currentpath=path.join([path])
                            self.procesarInfo(currentpath)
                        console.log(f' proceso exitoso,validar archivo: {path[:-3]}{sep}log')
                     #     console.print(" [ERROR: ][bold red]]'NO se TIENE BASES:")
                except ValueError as e:
                    console.print(" [ERROR: ][bold red] No se tiene Habilitado Modulo de GDD [\]", e)


    #2022 09 15 03 45 02

    def xst (self):
        from dateutil import parser,tz

        self.config.user=self.dato.ContenedorDZ[0]
        self.__ftp_client:IFtp =  ImplicitFTPTLS() if self.config.protocol== 'FTPS' else  SFTP_()
        self.__ftp_client.acceso(
            self.config.host,
            *self.config.CredencialesFtp
            )

        lines = []

        self.__ftp_client.change_dir("/COMUNES")
        self.__ftp_client.list_dir(lines.append)

        latest_time = None
        latest_name = None

        for line in lines:
            tokens = line.split(maxsplit = 9)
            time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
            time = parser.parse(time_str,tzinfos =tz.gettz('Ecuador'))
            # if (latest_time is None) or (time > latest_time):
            latest_name = tokens[8]
            latest_time = time
            print(latest_name,latest_time)

    def ds(self):
        print()

        self.config.user=self.dato.ContenedorDZ[0]
        self.__ftp_client:IFtp =  ImplicitFTPTLS() if self.config.protocol== 'FTPS' else  SFTP_()
        self.__ftp_client.acceso(
            self.config.host,
            *self.config.CredencialesFtp
            )

        d = self.__ftp_client.mlsd('/COMUNES')
        for i,v in d:
            print(i,v['modify'])


        self.__ftp_client.change_dir('/COMUNES')
        self.__ftp_client.list_dir()

#       self.__ftp_client.cdir('COMUNES')
#        print(self.__ftp_client.nlst())
        return d

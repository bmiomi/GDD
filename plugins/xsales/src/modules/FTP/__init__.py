from datetime import date, datetime, timedelta
from ftplib import FTP_TLS
import ssl
from paramiko import Transport,SFTP
from sqlite3 import  connect
from typing import List, Protocol
from plugins.xsales.src.modules.FTP.config import ConfigFtp

from plugins.xsales.util import descomprimir,sep


linea = '-' * 60

class IFtp(Protocol):

    def dir(self):
        raise NotImplemented

    def acceso(self, *arg):
        raise NotImplemented

    def change_dir(self, dir: str):
        raise NotImplemented

    def list_dir(self, *arg):
        raise NotImplemented

class DataConn:
    """"""
    def __init__(self, db_name):
        """Constructor"""
        self.db_name = db_name

    def __enter__(self):
        """
        Open the database connection
        """
        self.conn = connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection
        """
        self.conn.close()
        if exc_val:
            raise

class SFTP_(Transport):

    sftp = None
    files=[]

    def __init__(self):
        super().__init__(('200.31.27.104', 22))

    def acceso(self, *arg):
        self.connect(username=arg[1], password=arg[2])
        self.sftp = SFTP.from_transport(self)

    def change_dir(self, dir):
        self.sftp.chdir(dir)

    def list_dir(self,*args):
        return self.sftp.listdir(*args)

    def mostrarar_achivos(self,excluide=None):

        self.change_dir('PROD')
        
        for i in [i for i in self.list_dir() if  i not in excluide]:
            path=self.sftp.getcwd()
            file_date=self.sftp.stat(path+'/'+i).st_mtime
            last_modified_ts = datetime.fromtimestamp(file_date)
            last_modified_date = datetime.fromtimestamp(file_date).date() 
            last_modified_time = datetime.fromtimestamp(file_date).time()
            day=date.today()-timedelta(days=1)
            if last_modified_date != day and last_modified_time>=datetime.strptime("22:30:00","%H:%M:%S").time()  :
                self.files.append({'file':i,'fecha':last_modified_ts.strftime("%Y-%m-%d %H:%M:%S")})
               
class ImplicitFTPTLS(FTP_TLS):

    """FTP_TLS subclass that automatically wraps sockets in SSL to support implicit FTPS."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def change_dir(self, dir: str):
        return self.cwd(dir)

    def list_dir(self, *args):
        return self.dir(*args)

    def acceso(self, *args):
        self.connect(host=args[0], port=990, timeout=18000)
        self.login(args[1], args[2])

    def mostrarar_achivos(self, excluide=None):
        from dateutil import parser,tz
        f=[] 
        self.change_dir('/COMUNES')
        self.list_dir(f.append)
        for line in f:
            tokens = line.split(maxsplit = 9)
            time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
            time = parser.parse(time_str,tzinfos =tz.gettz('Quito'))
            latest_name = tokens[8]
            latest_time = time
            print(f"file: {latest_name} fecha {latest_time}" )

class FtpXsales:

    """

        Conexion con el Ftp de Xsales

    """
    status=''
    title=''

    def __init__(self) -> None:
        self.dato=None

        self.config=ConfigFtp()
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

    def mostrar_info(self,dz):

        self.config.operacion=self.dato.Opcion

        self.config.user=dz
        self.__ftp_client:IFtp =  ImplicitFTPTLS() if self.config.protocol== 'FTPS' else  SFTP_()
        self.__ftp_client.acceso(
            self.config.host,
            *self.config.CredencialesFtp
            )

        if self.dato.Opcion=='Validar Maestros':
            self.maestrosftp()
            self.dato.console.log(self.__ftp_client.files)
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
                    return f' proceso exitoso,validar archivo: {path[:-3]}{sep}log'
                # else:
                #     console.print(" [ERROR: ][bold red]]'NO se TIENE BASES:")
            except ValueError as e:
                self.dato.console.print(" [ERROR: ][bold red] No se tiene Habilitado Modulo de GDD [\]", e)


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

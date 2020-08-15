import ftplib
import os
import ssl
import sys
import zipfile
import sqlite3
from sqlite3 import Error
from Config.config import configuracion

linea = '-' * 60

#conexion con la base de datos
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
 
## consulta a la base de datos.
def select_tasks(conn, table,archivo):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM "+table)
 
    rows = cur.fetchall()
    for row in rows:
        archivo.write("REGISTROS EN "+table+": "+str(row[0])+'\n')
    return rows

class ImplicitFTP_TLS(ftplib.FTP_TLS):
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

class FtpXsales:

    """Conexion con el Ftp de Xsales para la Extración
        de archivos main de los diferentes dDz
    """

    def __init__(self):
        self.__ftp_client = ImplicitFTP_TLS()
        self.configuracion=configuracion()
        self.__rutas=[]
        self.rutascero=[]


    def Login (self):
        try:    
            if self.configuracion.USER is not None:
                print(f'Dz A Revisar,{self.configuracion.USER}')        
                self.__ftp_client.connect(host='prd1.xsalesmobile.net', port=990, timeout=180)
                self.__ftp_client.login(user=self.configuracion.USER, passwd=self.configuracion.PASS)
                self.__ftp_client.prot_p()
                return self.__ftp_client.getwelcome()
            else:
                self.configuracion._parser.error('Se requiere Argumentos.')            
        except ftplib.error_perm as e:
            print('error credenciales incorrectas')
            return  e

    @property
    def _rutas(self):
        return self.__rutas

    def folderDownloadXsales(self):
        self.__ftp_client.cwd('XSales_Replication/Download/')
        dirs = []
        self.__ftp_client.dir(dirs.append)
        self.__rutas=[ filename[49:]  for filename in dirs if filename[49:] != 'Backup'] 
        return self.__rutas

    def parseandorutas(self):
        return list(dict(name=i) for i in self.folderDownloadXsales())

    def DESCARGA(self,ruta):
        Xsalespath='\\XSales_Replication\\Download\\'+ruta+'\\'
        self.__ftp_client.cwd(Xsalespath)
        with open(self.configuracion.directorioRuta(ruta)+'\\'+'Main.zip','wb') as file: 
            self.__ftp_client.retrbinary('RETR '+'Main.zip', file.write)
         
    def descomprimir(self,ruta):
        with zipfile.ZipFile(f"{self.configuracion.directorioRuta(ruta)}\\Main.zip","r") as zip_ref:
            zip_ref.extractall(self.configuracion.directorioRuta(ruta))


    def procesarInfo(self,ruta):

       if   not os.path.isfile(self.configuracion.getpath+'\\logo'):
           archivo=open(self.configuracion.getpath+'\\logo','w')
       else:
           archivo=open(self.configuracion.getpath+'\\logo','a')
       database = self.configuracion.directorioRuta(ruta)+"\\Main.sqlite"
       conn = create_connection(database)
       with conn:
           archivo.write(linea+'\n')
           archivo.write("Ruta: "+ruta+'\n')
           ds=select_tasks(conn, "DISCOUNTDETAIL",archivo)
           dr=select_tasks(conn, "DISCOUNTROUTE",archivo)
           if ds[0][0] == 0 and dr[0][0]==0:
               self.rutascero.append(dict(ruta=ruta,descuento=ds[0][0],descRuta=dr[0][0]))
           if len(self.rutascero)>3:
                raise Exception(' Rutas con modulos Bloqueado')
       archivo.close()      


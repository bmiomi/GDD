"""
Módulo FTP - Gestión de archivos vía FTP/SFTP.
"""
from plugins.xsales.src.modules.base_module import XSalesModule, ModuleMetadata
from plugins.xsales.src.modules.module_registry import ModuleRegistry
from plugins.xsales.src.modules.Ftp.config import ConfigFtp
from typing import Any


@ModuleRegistry.register
class FtpModule(XSalesModule):
    """
    Módulo para operaciones FTP.
    
    Funcionalidades:
    - Descarga de archivos desde FTP
    - Validación de bases de datos
    - Validación de maestros
    """
    
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="ftp",
            display_name="FTP - Gestión de Archivos",
            description="Descarga y validación de archivos FTP",
            version="1.0.0",
            enabled=False
        )
    
    def setup(self, context) -> bool:
        """Inicialización del módulo FTP"""
        super().setup(context)
        self.config = ConfigFtp()
        self.config.Revisiones = 'Ftp'
        return True
    
    def run(self, context) -> Any:
        """Ejecución principal del módulo FTP"""
        from .interface.IFtp import IFtp
        from .ftp import ImplicitFTPTLS
        from .sftp import SFTP_
        from plugins.xsales.inputquestion import preguntass
        
        # Realizar preguntas específicas de FTP
        self.dato = preguntass(
            context.questionary,
            self.config
        )
        
        # Inicializar cliente FTP
        self.__ftp_client: IFtp = (
            ImplicitFTPTLS() 
            if self.config.protocol == 'FTPS' 
            else SFTP_()
        )
        
        # Mostrar información
        self.mostrar_info(
            self.dato.ContenedorDZ,
            context.console
        )
        
        # Generar archivo si se solicitó
        if self.dato.reporte:
            self.generararchivo(
                self.dato.reporte,
                self.dato.Opcion,
                context.console
            )
        
        return {"status": "success", "data": self.dato}
    
    def mostrar_info(self, dz, console):
        """Importar lógica del módulo FTP existente"""
        # Importar código existente de FTP/__init__.py
        from .enums.enumftp import Enumftp
        import questionary
        
        self.config.operacion = self.dato.Opcion
        self.config.user = dz[0]
        self.__ftp_client.acceso(self.config.host, *self.config.CredencialesFtp)
        
        if self.dato.Opcion == Enumftp.Validar_Maestros.value:
            self.maestrosftp()
            console.log(self.__ftp_client.files)
        
        if self.dato.Opcion == Enumftp.Validar_DESC.value:
            _rutas = self.listbases()
            lista_rutas = questionary.checkbox(
                "Seleccione las bases a descargar",
                choices=_rutas
            ).ask()

            with console.status('Procesando', spinner=self.config.spinner):
                try:
                    self.procesar_info(lista_rutas, console)
                except ValueError as e:
                    console.print(r" [ERROR: ][bold red] No se tiene Habilitado Modulo de GDD [\]", e)
                except BaseException as e:
                    console.print(f"[red]✗ Error FTP: {e.__class__.__name__}")
    
    def listbases(self):
        """Lista bases disponibles en FTP"""
        dirs = []
        self.__ftp_client.change_dir(self.config.pathdownload)
        self.__ftp_client.list_dir(lambda x: dirs.extend(x.splitlines()))
        return [
            filename[49:] 
            for filename in dirs 
            if not filename[49:].startswith('T') 
            and filename[49:] not in self.config.excluide
        ]
    
    def maestrosftp(self):
        """Muestra archivos maestros del FTP"""
        self.__ftp_client.mostrarar_achivos(excluide=self.config.xmlfile)

    def procesar_info(self, lista_rutas, console):
        from plugins.xsales.util import descomprimir, sep

        if lista_rutas and len(lista_rutas) >= 1:
            for i in lista_rutas:
                dest_path = self.config.nuevacarpeta(
                    self.config.pathdistribudor,
                    self.config.user,
                    self.config.fecha,
                    i
                )
                self.__ftp_client.descarga(i, dest_path, self.config.downloadfilebaseruta)
                descomprimir(dest_path)
                self.procesar_base(dest_path)
                console.log(f' proceso exitoso,validar archivo: {dest_path[:-3]}{sep}log')
        else:
            console.print(" [ERROR: ][bold red] NO SE TINE RUTAS QUE ITERAR")

    def procesar_base(self, destinopath: str) -> None:
        from plugins.xsales.util import sep
        from plugins.xsales.src.service.dbservice.sqliteservices import DataConn

        origenpath = ''.join([i for i in destinopath.rsplit(sep)[-1]])
        database = destinopath + sep + "Main.sqlite"
        lista = []
        with DataConn(database) as conn:
            for table in self.config.tablevalidacion:
                result = conn.execute(
                    f"SELECT COUNT(*) FROM  {table} WHERE DISCODE NOT LIKE 'DES%'"
                )
                result, = result.fetchone()
                lista.append({'Tabla': table, 'Ruta': origenpath, 'registros': result})
    
    def generararchivo(self, reporte, opcion, console):
        """Genera archivos de reporte"""
        # Lógica de generación de archivo
        pass
    
    def cleanup(self) -> None:
        """Limpieza de conexión FTP"""
        if hasattr(self, '__ftp_client'):
            try:
                # Cerrar conexión FTP
                pass
            except:
                pass

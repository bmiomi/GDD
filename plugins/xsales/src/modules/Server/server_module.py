"""
Módulo Server - Consultas y gestión de servidor XSales.
"""
from plugins.xsales.src.modules.base_module import XSalesModule, ModuleMetadata
from plugins.xsales.src.modules.module_registry import ModuleRegistry
from plugins.xsales.src.modules.Server.config import ConfigServer
from typing import Any


@ModuleRegistry.register
class ServerModule(XSalesModule):
    """
    Módulo para consultas al servidor XSales.
    
    Funcionalidades:
    - Consultas SQL a base de datos XSales
    - Validación de clientes
    - Reportes de pedidos
    - Revisiones de madrugada
    """
    
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="server",
            display_name="Server - Consultas XSales",
            description="Consultas y reportes del servidor XSales",
            version="1.0.0"
        )
    
    def __init__(self):
        """Constructor del módulo Server"""
        super().__init__()
        self._config = ConfigServer()
        self._config.Revisiones = 'Server'
        self.validadorsql = None
        self.contenedor = []
        self.contador = 0
    
    def setup(self, context) -> bool:
        """Inicialización del módulo Server"""
        super().setup(context)
        return True
    
    def run(self, context) -> Any:
        """Ejecución principal del módulo Server"""
        from plugins.xsales.inputquestion import preguntass
        
        # Realizar preguntas específicas de Server
        self.dato = preguntass(
            context.questionary,
            self._config
        )
        
        # Mostrar información
        self.mostrar_info(
            self.dato.ContenedorDZ,
            context.console
        )
        
        # Generar archivo si se solicitó
        self.generararchivo(
            self.dato.reporte,
            self.dato.Opcion,
            context.console
        )
        
        return {"status": "success", "data": self.dato}
    
    def mostrar_info(self, nombresdz, console):
        """Procesa consultas para distribuidores"""
        from plugins.xsales.src.modules.Server.Pagedriver.xsalesbeta import Xsales
        
        with console.status('Procesando..', spinner=self._config.spinner):
            for nombredz in nombresdz:
                # Crear instancia de Xsales para cada distribuidor
                xsales = Xsales(name=nombredz)
                self.consulta_Basedatos(nombredz, xsales, console)
    
    def consulta_Basedatos(self, nombredz, xsales, console):
        """Ejecuta consulta a base de datos"""
        from plugins.xsales.src.modules.Server.User.validador import ValidatorSql
        from plugins.xsales.src.modules.Server.User.Consultas import consultas
        
        try:
            if xsales.estado:
                consultas.NDISTRIBUIDOR = xsales.name
                sql = consultas.consulta(
                    self.dato.Opcion,
                    self._config.configConsultas
                )()
                
                result = xsales.consulta_new_version(sql)
                self.contenedor.append(result[0])
                self.validadorsql = ValidatorSql(self.dato.Opcion, result)
                console.log(f'Revisión completada para {nombredz}')
        except BaseException as e:
            console.log(f"Error en {nombredz}: {e}")
    
    def generararchivo(self, respuesta, nombre: str, console):
        """Genera archivo Excel con los resultados"""
        if respuesta:
            # Verificar que existan datos para generar
            if not self.validadorsql:
                console.print('[yellow]⚠ No hay datos para generar el archivo.')
                return
            
            if not hasattr(self.validadorsql, 'DZCOMPLETO') or not self.validadorsql.DZCOMPLETO:
                console.print('[yellow]⚠ No hay datos completos.')
                return
            
            try:
                from plugins.xsales.src.modules.Server.User.validador import ValidatorSql
                archivo = self._config.path.join(self._config.folderMadrugada, f'{nombre}')
                self._config.excelfile.create_file(archivo, self.validadorsql.DZCOMPLETO)
                console.print(f'[green]✓ Archivo generado: {archivo}')
                
                if hasattr(ValidatorSql, 'DZCOMPLETO'):
                    del ValidatorSql.DZCOMPLETO
            except Exception as e:
                console.print(f'[red]✗ Error al generar archivo: {e}')
    
    def cleanup(self) -> None:
        """Limpieza del módulo Server"""
        # No hay sesión HTTP que cerrar porque Xsales se instancia en cada ejecución
        pass

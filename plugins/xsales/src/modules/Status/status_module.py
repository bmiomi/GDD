"""
Módulo Status - Monitoreo de estado de rutas.
"""
from plugins.xsales.src.modules.base_module import XSalesModule, ModuleMetadata
from plugins.xsales.src.modules.module_registry import ModuleRegistry
from plugins.xsales.src.modules.Status.config import ConfigStatus
from plugins.xsales.src.modules.Status.Status import Status as StatusImpl
from typing import Any


@ModuleRegistry.register
class StatusModule(XSalesModule):
    """
    Módulo para monitoreo de estado de rutas.
    
    Funcionalidades:
    - Consulta de estado de rutas de distribución
    - Visualización de rutas en bajada
    - Reportes de estado
    """
    
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="status",
            display_name="Status - Estado de Rutas",
            description="Monitoreo de estado de rutas de distribución",
            version="1.0.0"
        )
    
    def setup(self, context) -> bool:
        """Inicialización del módulo Status"""
        super().setup(context)
        self.config = ConfigStatus()
        self.config.Revisiones = 'Status'
        self._status_impl = StatusImpl()
        return True
    
    def run(self, context) -> Any:
        """Ejecución principal del módulo Status"""
        from plugins.xsales.inputquestion import preguntass
        
        # Realizar preguntas específicas de Status
        self.dato = preguntass(
            context.questionary,
            self.config
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
    
    def mostrar_info(self, namedz, console):
        """Muestra información de estado de rutas"""
        self._status_impl.validardz(namedz)
        
        from rich.live import Live
        
        with Live(self._status_impl.generar_table(), console=console, refresh_per_second=4):
            while not self._status_impl.estado:
                self._status_impl.validardz(namedz)
                console.log(f'Rutas pendientes: {len(self._status_impl.dzincompletos)}')
    
    def generararchivo(self, reporte, opcion, console):
        """Genera archivo de reporte de status"""
        # Lógica de generación de archivo
        pass
    
    def cleanup(self) -> None:
        """Limpieza del módulo Status"""
        pass

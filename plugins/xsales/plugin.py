"""
Plugin de XSales con arquitectura de submódulos extensible.
"""
from core.Interfaces.plugin import IPlugin, PluginMetadata
from core.plugin_context import PluginContext
from typing import Any


class XSalesPlugin(IPlugin):
    """
    Plugin principal de XSales.
    
    Gestiona submódulos (FTP, Server, Status, etc.) mediante
    un sistema de registry que permite agregar nuevos módulos
    sin modificar código existente.
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="xsales",
            version="2.0.0",
            description="Automatización de XSales con submódulos extensibles",
            author="PRONACA Team",
            dependencies=["requests-html", "pandas", "openpyxl"]
        )
    
    def setup(self, context: PluginContext) -> bool:
        """Inicialización del plugin"""
        self._context = context
        self._console = context.console
        
        # Importar y inicializar factory de submódulos
        try:
            from plugins.xsales.src.modules import module_registry
            
            # Autodescubrir submódulos
            discovered = module_registry.autodiscover()
            
            if discovered:
                self._console.log(
                    f"[blue]→ XSales: {len(discovered)} submódulo(s) cargado(s)"
                )
            else:
                self._console.log("[yellow]⚠ XSales: No se encontraron submódulos")
            
            self._module_registry = module_registry
            
            return True
            
        except Exception as e:
            import traceback
            self._console.print(f"[red]✗ Error inicializando XSales: {e}[/red]")
            traceback.print_exc()
            return False
    
    def execute(self) -> Any:
        """Ejecución del plugin"""
        try:
            # Obtener lista de submódulos disponibles
            modules = self._module_registry.list_modules()
            
            if not modules:
                self._console.print("[yellow]⚠ No hay submódulos disponibles")
                return None
            
            # Crear opciones para el menú
            choices = self._module_registry.get_choices()
            
            # Usuario selecciona submódulo
            selection = self._context.questionary.rawselect(
                message="Que Sub Modulo de Xsales desea?",
                choices=choices
            ).ask()
            
            if selection is None:
                return None
            
            # Obtener nombre interno del módulo
            module_name = next(
                m.name for m in modules 
                if m.display_name == selection
            )
            
            # Obtener y ejecutar submódulo
            module = self._module_registry.get(module_name)
            
            # Setup del submódulo
            if not module.setup(self._context):
                self._console.print("[red]✗ Setup del submódulo falló[/red]")
                return None
            
            # Validar submódulo
            valid, msg = module.validate()
            if not valid:
                self._console.print(f"[yellow]⚠ Validación: {msg}[/yellow]")
                # Continuar de todas formas (por ahora)
            
            # Ejecutar submódulo
            result = module.run(self._context)
            
            # Limpiar submódulo
            module.cleanup()
            
            return result
            
        except KeyboardInterrupt:
            self._console.print("\n[yellow]→ Operación cancelada[/yellow]")
            return None
        except Exception as e:
            self._console.print(f"[red]✗ Error en submódulo: {e}[/red]")
            import traceback
            traceback.print_exc()
            return None
    
    def teardown(self) -> None:
        """Limpieza del plugin"""
        # Nada específico que limpiar por ahora
        pass
    
    def validate(self) -> tuple[bool, str]:
        """Validación del plugin"""
        # Validar que existan submódulos
        if hasattr(self, '_module_registry'):
            modules = self._module_registry.list_modules()
            if not modules:
                return False, "No hay submódulos disponibles"
        
        return True, "OK"

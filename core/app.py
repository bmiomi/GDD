"""
Aplicación principal con arquitectura de plugins mejorada.
"""
import os
import questionary
from rich.console import Console
from typing import Optional
from pathlib import Path

from .plugin_registry import PluginRegistry
from .plugin_context import PluginContext
from .config_manager import config_manager
from .Interfaces.plugin import PluginStatus


class MyApplication:
    """
    Aplicación principal con arquitectura de plugins mejorada.
    
    Características:
    - Descubrimiento automático de plugins
    - Inyección de dependencias via PluginContext
    - Lifecycle completo de plugins (setup → validate → execute → teardown)
    - Configuración centralizada
    - Interfaz de usuario rica con Rich
    
    Uso:
        app = MyApplication()
        app.run()
    """
    
    VERSION = '0.2.0'
    
    def __init__(self, workspace_path: Optional[str] = None):
        """
        Inicializa la aplicación.
        
        Args:
            workspace_path: Ruta del workspace (por defecto: directorio actual)
        """
        self.console = Console()
        self.plugin_registry = PluginRegistry(console=self.console)
        self._current_plugin: Optional[str] = None
        self.workspace_path = workspace_path or str(Path.cwd())
        
        # Banner de bienvenida
        self._show_banner()
        
        # Descubrir plugins
        self._discover_plugins()
    
    def _show_banner(self):
        """Muestra banner de bienvenida"""
        self.console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        self.console.print(f"[bold cyan]  GDD - PRONACA  v{self.VERSION}[/bold cyan]")
        self.console.print(f"[bold cyan]  Sistema de Gestión y Automatización[/bold cyan]")
        self.console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
    
    def _discover_plugins(self):
        """Descubre y carga plugins"""
        self.console.log("[blue]→ Descubriendo plugins...")
        
        discovered = self.plugin_registry.discover()
        
        if discovered:
            self.console.log(f"[green]✓ {len(discovered)} plugin(s) cargado(s)")
        else:
            self.console.log("[yellow]⚠ No se encontraron plugins")
    
    def create_context(self, plugin_name: str) -> PluginContext:
        """
        Crea contexto para ejecución de plugin.
        
        Args:
            plugin_name: Nombre del plugin
        
        Returns:
            PluginContext con dependencias inyectadas
        """
        # Obtener configuración del plugin si existe
        plugin_config = {}
        try:
            if plugin_name == 'xsales':
                # Cargar config específica de XSales
                from plugins.xsales.src.config import Config
                config_instance = Config()
                plugin_config = config_instance.config
        except:
            pass
        
        return PluginContext(
            console=self.console,
            questionary=questionary,
            config=plugin_config,
            shared_data={},
            workspace_path=self.workspace_path
        )
    
    def run(self):
        """Bucle principal de la aplicación"""
        while True:
            try:
                # Listar plugins disponibles
                plugins = self.plugin_registry.list_plugins()
                
                if not plugins:
                    self.console.print("[red]✗ No hay plugins disponibles")
                    break
                
                # Crear opciones para el menú
                choices = [p.name for p in plugins]
                choices.append("Salir")
                
                # Mostrar menú
                selection = questionary.rawselect(
                    message="SELECCIONE EL MODULO A USAR:",
                    choices=choices
                ).ask()
                
                if selection == "Salir" or selection is None:
                    self.console.print("\n[yellow]→ Saliendo del sistema...[/yellow]")
                    break
                
                # Ejecutar plugin seleccionado
                result = self.execute_plugin(selection)
                if isinstance(result, dict) and result.get("status") == "exit":
                    self.console.print("\n[yellow]→ Saliendo del sistema...[/yellow]")
                    break
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]→ Operación cancelada por el usuario[/yellow]")
                continue
            except Exception as e:
                self.console.print(f"[red]✗ Error: {e}[/red]")
                import traceback
                traceback.print_exc()
    
    def execute_plugin(self, plugin_name: str):
        """
        Ejecuta un plugin completo con su lifecycle.
        
        Args:
            plugin_name: Nombre del plugin a ejecutar
        """
        try:
            # Obtener plugin
            plugin = self.plugin_registry.get(plugin_name)
            plugin.status = PluginStatus.ACTIVE
            
            # Crear contexto
            context = self.create_context(plugin_name)
            
            self.console.log(f"[blue]→ Iniciando {plugin.metadata}...")
            
            # Setup
            if not plugin.setup(context):
                self.console.print("[red]✗ Setup del plugin falló[/red]")
                return
            
            # Validar
            valid, msg = plugin.validate()
            if not valid:
                self.console.print(f"[red]✗ Validación falló: {msg}[/red]")
                return
            
            # Ejecutar
            result = plugin.execute()
            
            # Teardown
            plugin.teardown()
            
            plugin.status = PluginStatus.LOADED

            return result
            
            return result
            
        except Exception as e:
            self.console.print(f"[red]✗ Error ejecutando {plugin_name}: {e}[/red]")
            
            # Asegurar teardown incluso en error
            try:
                plugin.teardown()
            except:
                pass
            
            raise
    
    @classmethod
    def start(cls):
        """
        Punto de entrada principal de la aplicación.
        Método estático para compatibilidad con código existente.
        """
        app = cls()
        app.run()


"""
Módulo Server - Consultas y gestión de servidor XSales.
REFACTORIZADO con Clean Architecture.
"""
from plugins.xsales.src.modules.base_module import XSalesModule, ModuleMetadata
from plugins.xsales.src.modules.module_registry import ModuleRegistry
from typing import Any, List, Dict
import logging

from core.wizard import PreferenceWizard
from core.config import PreferencesManager
from core.models import PreferenceData

from .di_container import ServerModuleDIContainer
from .presenters import ExcelPresenter, ConsolePresenter
from .navigation import NavigationController
from .services import EditPreferencesUseCase

logger = logging.getLogger(__name__)


@ModuleRegistry.register
class ServerModule(XSalesModule):
    """
    Módulo para consultas al servidor XSales.
    
    Responsabilidades (REDUCIDAS):
    - Setup inicial y wizard de preferencias
    - Orquestar ejecución delegando a Use Cases
    - NO más lógica de negocio (movida a Use Cases)
    """
    
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="server",
            display_name="Server - Consultas XSales",
            description="Consultas y reportes del servidor XSales",
            version="2.0.0"  # ← Actualizado con Clean Architecture
        )
    
    def __init__(self):
        """Constructor del módulo Server"""
        super().__init__()
        self.prefs_manager = PreferencesManager()
        self.preferences: PreferenceData = None
        self.di_container: ServerModuleDIContainer = None
    
    def setup(self, context) -> bool:
        """
        Inicialización del módulo Server.
        - Carga o crea preferencias
        - Inicializa DI Container
        """
        super().setup(context)
        
        # 1. Gestionar preferencias
        if not self.prefs_manager.exists(self.metadata.name):
            wizard = PreferenceWizard(context.console)
            self.preferences = wizard.run(self.metadata.name)
            self.prefs_manager.save(self.metadata.name, self.preferences)
        else:
            self.preferences = self.prefs_manager.load(self.metadata.name)
        
        # 2. Inicializar DI Container con preferencias
        self.di_container = ServerModuleDIContainer(
            preferences=self.preferences
        )
        
        logger.info(f"✓ {self.metadata.display_name} inicializado")
        return True
    
    def run(self, context) -> Any:
        """
        Ejecución principal del módulo Server con navegación.
        Usa NavigationController para manejar flujo entre pantallas.
        """
        from plugins.xsales.inputquestion import menu_principal
        from plugins.xsales.src.modules.Server.config import ConfigServer
        
        navigator = NavigationController()
        config = ConfigServer()
        config.Revisiones = 'Server'
        
        # Loop de navegación
        while True:
            current_screen = navigator.get_current()
            
            if current_screen == "main_menu":
                dato = menu_principal(
                    context.questionary,
                    config,
                    self.preferences
                )
                
                if dato.action == 'configure':
                    navigator.navigate_to("configure_menu")
                elif dato.action == 'query':
                    # Ejecutar consultas
                    self._execute_queries(
                        distributors=dato.ContenedorDZ,
                        query_option=dato.Opcion,
                        user_params=dato.parametros_usuario or {},
                        turno=dato.Turno,
                        console=context.console
                    )
                    break  # Salir después de ejecutar
                else:
                    break
            
            elif current_screen == "configure_menu":
                action = self._show_configure_menu(context)
                
                if action == "edit_preferences":
                    navigator.navigate_to("edit_preferences_menu")
                elif action == "edit_queries":
                    navigator.navigate_to("edit_queries_menu")
                elif action == "back_to_main":
                    navigator.go_back()
                    break
            
            elif current_screen == "edit_preferences_menu":
                self._edit_preferences(context)
                navigator.go_back()
            
            elif current_screen == "edit_queries_menu":
                self._edit_queries(context)
                navigator.go_back()
        
        return {"status": "success"}
    
    def _show_configure_menu(self, context) -> str:
        """
        Menú principal de configuración.
        
        Returns:
            Acción seleccionada: "edit_preferences", "edit_queries", "back_to_main"
        """
        action = context.questionary.select(
            "⚙️  Configuración",
            choices=[
                '🎨 Cambiar presentación visual (formato, Excel, logs)',
                '📝 Gestionar consultas',
                '↩️  Volver al menú principal'
            ]
        ).ask()
        
        if '🎨 Cambiar presentación visual' in action:
            return "edit_preferences"
        elif '📝 Gestionar consultas' in action:
            return "edit_queries"
        else:
            return "back_to_main"
    
    def _edit_preferences(self, context):
        """Editar preferencias de visualización."""
        use_case = EditPreferencesUseCase(
            prefs_repo=self.prefs_manager,
            console=context.console
        )
        
        self.preferences = use_case.execute('server')
        
        # Actualizar el DI Container con nuevas preferencias
        if self.di_container:
            self.di_container.preferences = self.preferences
    
    def _edit_queries(self, context):
        """Gestionar consultas personalizadas."""
        from core.wizard import QueryWizard
        from core.config import QueriesManager
        
        context.console.print("[bold cyan]\n📝 Gestionar Consultas[/bold cyan]")
        
        queries_manager = QueriesManager()
        
        while True:
            accion = context.questionary.select(
                "¿Qué deseas hacer?",
                choices=[
                    'Crear nueva consulta',
                    'Ver consultas guardadas',
                    'Eliminar consulta',
                    '↩️  Volver'
                ]
            ).ask()
            
            if accion == 'Crear nueva consulta':
                wizard = QueryWizard(context.console)
                query = wizard.run()
                
                if query:
                    queries_manager.save(self.metadata.name, query)
                    context.console.print(f"[green]✓ Consulta '{query.name}' guardada[/green]")
            
            elif accion == 'Ver consultas guardadas':
                queries = queries_manager.load_all(self.metadata.name)
                if queries:
                    context.console.print("[cyan]Consultas personalizadas:[/cyan]")
                    for name in queries.keys():
                        context.console.print(f"  • {name}")
                else:
                    context.console.print("[yellow]No hay consultas personalizadas[/yellow]")
            
            elif accion == 'Eliminar consulta':
                queries = queries_manager.load_all(self.metadata.name)
                if queries:
                    query_name = context.questionary.select(
                        "¿Cuál eliminar?",
                        choices=list(queries.keys())
                    ).ask()
                    
                    queries_manager.delete(self.metadata.name, query_name)
                    context.console.print(f"[green]✓ Consulta '{query_name}' eliminada[/green]")
            
            elif '↩️  Volver' in accion:
                break
    
    def _handle_configure(self, context) -> Any:
        """DEPRECATED - Usar _show_configure_menu() en su lugar."""
        return self._show_configure_menu(context)
    
    def _execute_queries(
        self,
        distributors: List[str],
        query_option: str,
        user_params: Dict[str, str],
        turno: str,
        console
    ):
        """
        Ejecuta consultas para múltiples distribuidores.
        ACUMULA todos los resultados en UNA SOLA presentación.
        """
        # 1. Preparar presenters según preferencias
        results_accumulated = []
        excel_presenter = None
        console_presenter = ConsolePresenter(console, output_format=self.preferences.output_format)
        
        if self.preferences and self.preferences.generate_excel:
            excel_presenter = ExcelPresenter(
                output_directory=self.preferences.excel_directory or './REPORTES/SERVER',
                open_when_done=self.preferences.open_excel_when_done
            )
        
        # 2. Ejecutar para cada distribuidor y acumular
        with console.status('Procesando consultas...', spinner='dots'):
            for distributor in distributors:
                try:
                    # Configurar DI Container para este distribuidor
                    self.di_container.set_distributor(distributor)
                    
                    # Agregar parámetros del sistema
                    all_params = dict(user_params)
                    all_params['NDISTRIBUIDOR'] = distributor
                    
                    logger.debug(f"Ejecutando para {distributor} con params: {all_params}")
                    
                    # Obtener Use Case
                    run_query = self.di_container.get_run_query_use_case()
                    
                    # Ejecutar consulta
                    result = run_query.execute(query_option, all_params)
                    
                    if result.is_success():
                        # Agregar distribuidor a cada fila
                        for row in result.rows:
                            if isinstance(row, dict):
                                row['Distribuidor'] = distributor
                            results_accumulated.append(row)
                    else:
                        console.log(f"[red]✗ Error en {distributor}: {result.error}[/red]")
                    
                except Exception as e:
                    console.log(f"[red]✗ Error en {distributor}: {e}[/red]")
                    logger.error(f"Error procesando {distributor}: {e}", exc_info=True)
        
        # 3. PRESENTAR TODO JUNTO (no uno por uno)
        if results_accumulated:
            console.print()  # Salto de línea
            
            # Presentar en la consola con el formato visual elegido
            console_presenter.present_multiple(
                query_name=query_option,
                rows=results_accumulated,
                distributors=distributors
            )
            
            # Si está habilitado, también acumular en Excel
            if excel_presenter:
                try:
                    excel_presenter.add_rows(results_accumulated)
                    filename = f"{query_option}_{turno}" if turno else query_option
                    file_path = excel_presenter.flush(filename)
                    if file_path:
                        console.print(f"[green]✓ Excel generado: {file_path}[/green]")
                except Exception as e:
                    console.print(f"[red]✗ Error generando Excel: {e}[/red]")
                    logger.error(f"Error generando Excel: {e}", exc_info=True)
        else:
            console.print("[yellow]⊘ Sin resultados[/yellow]")
    
    def cleanup(self) -> None:
        """Limpieza del módulo Server"""
        # El DI Container maneja el cleanup de sus componentes
        pass

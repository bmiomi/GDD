"""
Configuración e inyección de dependencias para ServerModule.
Aquí se wirea todo: repositories, validators, executors, use cases.
"""
from pathlib import Path
from typing import Optional
from core.di_container import DIContainer
from core.config import PreferencesManager
from core.repositories import ResultPresenter
from core.ui import TablePresenter, ListPresenter, SummaryPresenter

from .infrastructure import XSalesHttpClient
from .presenters import ExcelPresenter
from .repositories import (
    YamlQueryRepository,
    XSalesQueryValidator,
    XSalesQueryExecutor,
)
from .services import (
    RunQueryUseCase,
    ConfigurePreferencesUseCase,
    CreateConsultaUseCase,
    ExportResultUseCase,
)


class ServerModuleDIContainer(DIContainer):
    """DI Container específico para ServerModule."""
    
    def __init__(
        self,
        config_path: str = None,
        distributor_name: str = None,
        preferences: 'PreferenceData' = None
    ):
        """
        Args:
            config_path: Ruta a config.yml con consultas
            distributor_name: Nombre del distribuidor para XSales
            preferences: Preferencias del usuario (para elegir presenter)
        """
        super().__init__()
        self.config_path = Path(config_path) if config_path else self._get_default_config_path()
        self.distributor_name = distributor_name
        self.preferences = preferences
        self._setup_dependencies()
    
    def _get_default_config_path(self) -> Path:
        """Obtiene ruta por defecto a config.yml de Server."""
        return Path(__file__).parent / 'config.yml'
    
    def _setup_dependencies(self):
        """Registra todas las dependencias."""
        
        # Infrastructure (HTTP Clients)
        if self.distributor_name:
            http_client = XSalesHttpClient(self.distributor_name)
            self.register_instance('XSalesHttpClient', http_client)
        
        # Repositories (acceso a datos)
        query_repo = YamlQueryRepository(str(self.config_path))
        self.register_instance('QueryRepository', query_repo)
        
        prefs_manager = PreferencesManager()
        self.register_instance('PreferencesRepository', prefs_manager)
        
        # Validators & Executors
        validator = XSalesQueryValidator()
        self.register_instance('QueryValidator', validator)
        
        def executor_factory():
            http_client = self.get('XSalesHttpClient') if self.distributor_name else None
            return XSalesQueryExecutor(http_client=http_client)
        self.register('QueryExecutor', executor_factory)
        
        # Presenters (salida de datos)
        self._setup_presenters()
        
        # Use Cases (lógica de aplicación)
        self._setup_use_cases()
    
    def _setup_presenters(self):
        """Configura presenters según preferencias."""
        # Presenter principal (para visualización)
        if self.preferences:
            format_type = self.preferences.output_format
        else:
            format_type = 'table'
        
        if format_type == 'list':
            presenter = ListPresenter()
        elif format_type == 'summary':
            presenter = SummaryPresenter()
        else:
            presenter = TablePresenter()
        
        self.register_instance('ResultPresenter', presenter)
        
        # Excel Presenter (para exportación)
        if self.preferences and self.preferences.generate_excel:
            excel_presenter = ExcelPresenter(
                output_directory=self.preferences.excel_directory or './REPORTES/SERVER',
                open_when_done=self.preferences.open_excel_when_done
            )
            self.register_instance('ExcelPresenter', excel_presenter)
    
    def _setup_use_cases(self):
        """Configura use cases."""
        def run_query_factory():
            return RunQueryUseCase(
                query_repo=self.get('QueryRepository'),
                validator=self.get('QueryValidator'),
                executor=self.get('QueryExecutor'),
                presenter=self.get('ResultPresenter'),
            )
        self.register('RunQueryUseCase', run_query_factory)
        
        def config_prefs_factory():
            return ConfigurePreferencesUseCase(
                prefs_repo=self.get('PreferencesRepository')
            )
        self.register('ConfigurePreferencesUseCase', config_prefs_factory)
        
        def create_consulta_factory():
            return CreateConsultaUseCase(
                query_repo=self.get('QueryRepository')
            )
        self.register('CreateConsultaUseCase', create_consulta_factory)
        
        def export_result_factory():
            # Usar ExcelPresenter si está configurado, sino ResultPresenter
            try:
                presenter = self.get('ExcelPresenter')
            except KeyError:
                presenter = self.get('ResultPresenter')
            
            return ExportResultUseCase(presenter=presenter)
        self.register('ExportResultUseCase', export_result_factory)
    
    def get_run_query_use_case(self) -> RunQueryUseCase:
        """Conveniencia: obtén el use case de ejecutar query."""
        return self.get('RunQueryUseCase')
    
    def get_configure_preferences_use_case(self) -> ConfigurePreferencesUseCase:
        """Conveniencia: obtén el use case de configurar preferencias."""
        return self.get('ConfigurePreferencesUseCase')
    
    def set_presenter(self, presenter: ResultPresenter):
        """Cambia dinámicamente el presenter (ej: TablePresenter → ExcelPresenter)."""
        self.register_instance('ResultPresenter', presenter)
    
    def set_distributor(self, distributor_name: str):
        """Cambia el distribuidor activo y actualiza el HTTP client."""
        self.distributor_name = distributor_name
        http_client = XSalesHttpClient(distributor_name)
        self.register_instance('XSalesHttpClient', http_client)
        
        # Recrear executor con nuevo cliente
        def executor_factory():
            return XSalesQueryExecutor(http_client=self.get('XSalesHttpClient'))
        self.register('QueryExecutor', executor_factory)

        # Recrear RunQueryUseCase para evitar caché con executor anterior
        def run_query_factory():
            return RunQueryUseCase(
                query_repo=self.get('QueryRepository'),
                validator=self.get('QueryValidator'),
                executor=self.get('QueryExecutor'),
                presenter=self.get('ResultPresenter'),
            )
        self.register('RunQueryUseCase', run_query_factory)

"""
Use Case: Exportar resultado (para ServerModule).
"""
from core.domain import QueryResult
from core.repositories import ResultPresenter


class ExportResultUseCase:
    """Exporta un resultado a diferentes formatos."""
    
    def __init__(self, presenter: ResultPresenter):
        self.presenter = presenter
    
    def execute(self, result: QueryResult) -> None:
        """
        Exporta un resultado.
        
        Args:
            result: QueryResult a exportar
        """
        if not result.is_success():
            self.presenter.present(result)
            return
        
        self.presenter.present(result)

"""
Presentador de tabla.
"""
from rich.table import Table
from rich.console import Console
from core.models import ResultData


class TablePresenter:
    """Muestra resultados como tabla con Rich."""
    
    def __init__(self, console: Console = None):
        self.console = console or Console()
    
    def present(self, result: ResultData):
        """Presentar resultado como tabla."""
        if not result.is_success():
            self.console.print(f"[red]Error: {result.error}[/red]")
            return
        
        if not result.rows:
            self.console.print("[yellow]No hay datos[/yellow]")
            return
        
        table = Table(title=f"Query: {result.query_name}")
        
        # Agregar columnas
        for col in result.columns:
            table.add_column(col, style="cyan")
        
        # Agregar filas
        for row in result.rows:
            table.add_row(*[str(row.get(col, '')) for col in result.columns])
        
        self.console.print(table)
        self.console.print(f"[green]✓ {result.total_rows} filas en {result.execution_time:.2f}s[/green]")

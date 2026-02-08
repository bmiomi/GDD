"""
Presentador de lista.
"""
from rich.console import Console
from core.models import ResultData


class ListPresenter:
    """Muestra resultados como lista con Rich."""
    
    def __init__(self, console: Console = None):
        self.console = console or Console()
    
    def present(self, result: ResultData):
        """Presentar resultado como lista."""
        if not result.is_success():
            self.console.print(f"[red]Error: {result.error}[/red]")
            return
        
        if not result.rows:
            self.console.print("[yellow]No hay datos[/yellow]")
            return
        
        self.console.print(f"[bold cyan]{result.query_name}[/bold cyan]")
        self.console.print(f"[dim]{result.total_rows} filas en {result.execution_time:.2f}s[/dim]\n")
        
        for i, row in enumerate(result.rows, 1):
            self.console.print(f"[bold yellow]{i}.[/bold yellow]")
            for col in result.columns:
                self.console.print(f"  {col}: {row.get(col, '')}")
            self.console.print()

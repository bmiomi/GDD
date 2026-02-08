"""
Presentador de resumen.
"""
from rich.console import Console
from rich.panel import Panel
from core.models import ResultData


class SummaryPresenter:
    """Muestra resumen de resultados con Rich."""
    
    def __init__(self, console: Console = None):
        self.console = console or Console()
    
    def present(self, result: ResultData):
        """Presentar resultado como resumen."""
        summary = result.get_summary()
        
        if not result.is_success():
            panel_content = f"[red]❌ {summary['error']}[/red]"
        else:
            panel_content = (
                f"[green]✓ Query:[/green] {summary['query']}\n"
                f"[cyan]📊 Filas:[/cyan] {summary['total_rows']}\n"
                f"[blue]⏱️  Tiempo:[/blue] {summary['execution_time']}"
            )
        
        panel = Panel(panel_content, title="Resultado")
        self.console.print(panel)

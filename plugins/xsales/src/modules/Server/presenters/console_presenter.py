"""
ConsolePresenter: Presenta resultados en consola con diferentes formatos.
"""
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from core.ui import TablePresenter, ListPresenter, SummaryPresenter


class ConsolePresenter:
    """
    Presenta múltiples resultados en la consola.
    Soporta: tabla, lista, resumen
    """
    
    def __init__(self, console: Console = None, output_format: str = 'table'):
        self.console = console or Console()
        self.output_format = output_format
    
    def present_multiple(
        self,
        query_name: str,
        rows: List[Dict[str, Any]],
        distributors: List[str]
    ):
        """
        Presenta múltiples filas de resultados.
        
        Args:
            query_name: Nombre de la consulta
            rows: Lista de filas con datos
            distributors: Distribuidores procesados
        """
        if not rows:
            self.console.print("[yellow]Sin resultados[/yellow]")
            return
        
        # Título
        self.console.print(f"\n[bold cyan]Query: {query_name}[/bold cyan]")
        self.console.print(f"[dim]Distribuidores: {', '.join(distributors)}[/dim]")
        self.console.print(f"[dim]Total filas: {len(rows)}[/dim]\n")
        
        # Presentar según formato
        if self.output_format == 'table':
            self._present_as_table(rows)
        elif self.output_format == 'list':
            self._present_as_list(rows)
        elif self.output_format == 'summary':
            self._present_as_summary(rows)
        else:
            self._present_as_table(rows)  # default
    
    def _present_as_table(self, rows: List[Dict[str, Any]]):
        """Presenta como tabla."""
        if not rows:
            return
        
        # Crear tabla
        table = Table(show_header=True, header_style="bold cyan")
        
        # Headers (de la primera fila)
        first_row = rows[0]
        for key in first_row.keys():
            table.add_column(key)
        
        # Rows
        for row in rows:
            values = [str(row.get(k, '')) for k in first_row.keys()]
            table.add_row(*values)
        
        self.console.print(table)
    
    def _present_as_list(self, rows: List[Dict[str, Any]]):
        """Presenta como lista."""
        for i, row in enumerate(rows, 1):
            self.console.print(f"\n[bold]{i}.[/bold]")
            for key, value in row.items():
                self.console.print(f"  {key}: {value}")
    
    def _present_as_summary(self, rows: List[Dict[str, Any]]):
        """Presenta resumen estadístico."""
        self.console.print(f"[cyan]📊 Resumen:[/cyan]")
        self.console.print(f"  • Total filas: {len(rows)}")
        
        # Mostrar primeras 5 filas
        self.console.print(f"\n[dim]Primeras 5 registros:[/dim]")
        for i, row in enumerate(rows[:5], 1):
            cols = ', '.join([f"{k}={v}" for k, v in list(row.items())[:3]])
            self.console.print(f"  {i}. {cols}")
        
        if len(rows) > 5:
            self.console.print(f"  ... y {len(rows) - 5} más")

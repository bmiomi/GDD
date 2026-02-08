"""
Asistente para crear/editar consultas personalizadas.
"""
from typing import Optional
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from core.models import QueryData


class QueryWizard:
    """Wizard para crear/editar consultas SQL con parámetros."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
    
    def run(self) -> Optional[QueryData]:
        """
        Ejecutar wizard de consulta.
        
        Returns:
            QueryData si es válida, None si cancela
        """
        self.console.print(Panel(
            "[bold cyan]📝 Nueva Consulta SQL[/bold cyan]",
            expand=False
        ))
        
        # Nombre
        name = questionary.text(
            "Nombre de la consulta:",
            validate=lambda x: len(x) > 0 or "Nombre requerido"
        ).ask()
        
        if not name:
            return None
        
        # Descripción
        descripcion = questionary.text(
            "Descripción (opcional):"
        ).ask()
        
        # SQL
        self.console.print("\n[dim]Ingresa tu SQL (usa {{param}} para parámetros):[/dim]")
        sql = questionary.text(
            "SQL:",
            multiline=True,
            validate=lambda x: len(x) > 0 or "SQL requerida"
        ).ask()
        
        if not sql:
            return None
        
        # Parámetros
        params_str = questionary.text(
            "Parámetros (separados por coma):",
            default=""
        ).ask()
        
        parametros = [p.strip() for p in params_str.split(',') if p.strip()]
        
        # Crear objeto
        query = QueryData(
            name=name,
            sql=sql,
            parametros_usuario=parametros,
            descripcion=descripcion
        )
        
        # Validar
        is_valid, message = query.validate()
        
        if is_valid:
            self.console.print(f"[green]✓ {message}[/green]")
            
            # Preview
            self.console.print("\n[dim]Preview:[/dim]")
            syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
            self.console.print(syntax)
            
            confirm = questionary.confirm(
                "¿Guardar consulta?"
            ).ask()
            
            return query if confirm else None
        else:
            self.console.print(f"[red]✗ {message}[/red]")
            retry = questionary.confirm(
                "¿Reintentar?"
            ).ask()
            
            return self.run() if retry else None

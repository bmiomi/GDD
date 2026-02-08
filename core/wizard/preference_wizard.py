"""
Asistente de configuración de preferencias.
"""
from typing import Optional
import questionary
from rich.console import Console
from rich.panel import Panel

from core.models import PreferenceData


class PreferenceWizard:
    """Wizard para configurar preferencias de un submódulo."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
    
    def run(self, module_name: str) -> PreferenceData:
        """
        Ejecutar wizard de preferencias.
        
        Args:
            module_name: Nombre del módulo (server, ftp, status)
        
        Returns:
            PreferenceData configurada
        """
        self.console.print(Panel(
            f"[bold cyan]⚙️  Configuración de {module_name.upper()}[/bold cyan]",
            expand=False
        ))
        
        # Formato de salida
        output_format = questionary.select(
            "¿Cómo mostrar resultados?",
            choices=['tabla', 'lista', 'resumen']
        ).ask()
        
        # Excel
        generate_excel = questionary.confirm(
            "¿Generar Excel por defecto?"
        ).ask()
        
        open_excel = False
        if generate_excel:
            open_excel = questionary.confirm(
                "¿Abrir Excel al terminar?"
            ).ask()
        
        # Logging
        log_level = questionary.select(
            "¿Nivel de log?",
            choices=['normal', 'debug']
        ).ask()
        
        show_sql = questionary.confirm(
            "¿Mostrar SQL antes de ejecutar?"
        ).ask()
        
        # Directorio
        excel_dir = questionary.text(
            "Directorio para Excel:",
            default='./REPORTES'
        ).ask()
        
        prefs = PreferenceData(
            output_format=output_format,
            generate_excel=generate_excel,
            open_excel_when_done=open_excel,
            log_level=log_level,
            show_sql=show_sql,
            excel_directory=excel_dir or './REPORTES'
        )
        
        self.console.print("[green]✓ Preferencias guardadas[/green]")
        return prefs

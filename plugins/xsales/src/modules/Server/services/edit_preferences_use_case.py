"""
Use Case: Editar preferencias existentes (para ServerModule).
"""
import logging
import questionary
from rich.console import Console
from typing import Optional, Any

from core.models import PreferenceData

logger = logging.getLogger(__name__)


class EditPreferencesUseCase:
    """
    Permite editar las preferencias de visualización y salida de un módulo.
    """
    
    def __init__(
        self, 
        prefs_repo: Any,  # PreferencesManager o cualquier objeto con load/save
        console: Optional[Console] = None
    ):
        self.prefs_repo = prefs_repo
        self.console = console or Console()
    
    def execute(self, module_name: str = 'server') -> PreferenceData:
        """
        Permite editar las preferencias existentes.
        
        Args:
            module_name: Nombre del módulo ('server', 'ftp', etc.)
        
        Returns:
            PreferenceData actualizada
        """
        # 1. Cargar preferencias actuales
        try:
            current_prefs = self.prefs_repo.load(module_name)
            if current_prefs is None:
                current_prefs = PreferenceData()
            elif isinstance(current_prefs, dict):
                current_prefs = PreferenceData.from_dict(current_prefs)
        except Exception as e:
            logger.warning(f"No se pudieron cargar preferencias: {e}")
            current_prefs = PreferenceData()
        
        self.console.print("\n[cyan]📋 Editar Preferencias[/cyan]\n")
        
        # 2. Mostrar opciones actuales
        self.console.print(f"[dim]Configuración actual:[/dim]")
        self.console.print(f"  • Formato: [bold]{current_prefs.output_format}[/bold]")
        self.console.print(f"  • Excel: [bold]{'Sí' if current_prefs.generate_excel else 'No'}[/bold]")
        self.console.print(f"  • Mostrar SQL: [bold]{'Sí' if current_prefs.show_sql else 'No'}[/bold]")
        self.console.print(f"  • Log level: [bold]{current_prefs.log_level}[/bold]\n")
        
        # 3. Permitir editar cada preferencia
        prefs_to_edit = questionary.checkbox(
            "¿Qué prefieres cambiar?",
            choices=[
                '📊 Formato de visualización (tabla/lista/resumen)',
                '📁 Generar Excel (sí/no)',
                '🔍 Mostrar SQL (sí/no)',
                '📝 Nivel de logs (normal/debug)',
                '↩️  Volver sin cambios',
            ]
        ).ask()
        
        if not prefs_to_edit or '↩️  Volver sin cambios' in prefs_to_edit:
            self.console.print("[yellow]⊘ Sin cambios[/yellow]")
            return current_prefs
        
        # 4. Procesar cambios
        if '📊 Formato de visualización (tabla/lista/resumen)' in prefs_to_edit:
            current_prefs.output_format = questionary.select(
                "Formato de visualización:",
                choices=['table', 'list', 'summary']
            ).ask() or current_prefs.output_format
        
        if '📁 Generar Excel (sí/no)' in prefs_to_edit:
            current_prefs.generate_excel = questionary.confirm(
                "¿Generar Excel por defecto?"
            ).ask()
            
            if current_prefs.generate_excel:
                current_prefs.open_excel_when_done = questionary.confirm(
                    "¿Abrir Excel al terminar?"
                ).ask()
        
        if '🔍 Mostrar SQL (sí/no)' in prefs_to_edit:
            current_prefs.show_sql = questionary.confirm(
                "¿Mostrar SQL antes de ejecutar?"
            ).ask()
        
        if '📝 Nivel de logs (normal/debug)' in prefs_to_edit:
            current_prefs.log_level = questionary.select(
                "Nivel de logs:",
                choices=['normal', 'debug']
            ).ask() or current_prefs.log_level
        
        # 5. Guardar cambios
        try:
            self.prefs_repo.save(module_name, current_prefs)
            self.console.print("[green]✓ Preferencias guardadas[/green]")
            logger.info(f"Preferencias actualizadas para {module_name}")
        except Exception as e:
            self.console.print(f"[red]✗ Error guardando preferencias: {e}[/red]")
            logger.error(f"Error guardando preferencias: {e}")
        
        return current_prefs

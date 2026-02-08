"""
ExcelPresenter - Genera archivos Excel desde QueryResult.
Implementa ResultPresenter para integrarse con la arquitectura.
"""
import os
import pandas as pd
from typing import Dict, List
from pathlib import Path
from core.repositories import ResultPresenter
from core.domain import QueryResult
import logging

logger = logging.getLogger(__name__)


class ExcelPresenter(ResultPresenter):
    """Presenter que genera archivos Excel en lugar de mostrar en pantalla."""
    
    def __init__(
        self,
        output_directory: str = './REPORTES/SERVER',
        group_by_attribute: str = None,
        open_when_done: bool = False
    ):
        """
        Args:
            output_directory: Directorio donde guardar archivos Excel
            group_by_attribute: Atributo para agrupar datos en hojas (ej: 'Turno')
            open_when_done: Si debe abrir el archivo al terminar
        """
        self.output_directory = Path(output_directory)
        self.group_by_attribute = group_by_attribute
        self.open_when_done = open_when_done
        self._accumulated_data: Dict[str, List[Dict]] = {}
        
        # Crear directorio si no existe
        self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def present(self, result: QueryResult) -> None:
        """
        "Presenta" el resultado generando un archivo Excel.
        
        Args:
            result: QueryResult con los datos
        """
        if not result.success:
            logger.error(f"No se puede generar Excel: Query falló - {result.error_message}")
            return
        
        if not result.rows:
            logger.warning("No hay datos para generar Excel")
            return
        
        # Acumular datos (por si se llama múltiples veces)
        group_key = self._get_group_key(result)
        if group_key not in self._accumulated_data:
            self._accumulated_data[group_key] = []
        
        self._accumulated_data[group_key].extend(result.rows)
        logger.debug(f"Acumulados {len(result.rows)} registros en grupo '{group_key}'")
    
    def flush(self, filename: str) -> str:
        """
        Escribe todos los datos acumulados a un archivo Excel.
        
        Args:
            filename: Nombre base del archivo (sin extensión)
        
        Returns:
            Ruta completa del archivo generado
        """
        if not self._accumulated_data:
            logger.warning("No hay datos acumulados para escribir")
            return None
        
        file_path = self.output_directory / f"{filename}.xlsx"
        
        try:
            # Generar Excel con múltiples hojas si hay agrupación
            if len(self._accumulated_data) > 1:
                self._write_multisheet(file_path)
            else:
                self._write_single_sheet(file_path)
            
            # También generar TXT consolidado
            self._write_txt(file_path.with_suffix('.txt'))
            
            logger.info(f"✓ Excel generado: {file_path}")
            
            # Abrir archivo si se configuró
            if self.open_when_done:
                self._open_file(file_path)
            
            # Limpiar datos acumulados
            self._accumulated_data = {}
            
            return str(file_path)
        
        except Exception as e:
            logger.error(f"Error generando Excel: {e}")
            raise
    
    def _get_group_key(self, result: QueryResult) -> str:
        """Obtiene la clave de agrupación de los datos."""
        if not self.group_by_attribute:
            return "default"
        
        # Intentar extraer del contexto del QueryResult
        # (Por ahora usamos un default, pero se puede extender)
        return getattr(result, self.group_by_attribute, "default")
    
    def _write_multisheet(self, file_path: Path):
        """Escribe Excel con múltiples hojas."""
        with pd.ExcelWriter(str(file_path), engine="openpyxl") as writer:
            for group_key, data in self._accumulated_data.items():
                if data:
                    df = pd.DataFrame(data)
                    # Normalizar nombre de hoja (max 31 caracteres)
                    sheet_name = self._sanitize_sheet_name(str(group_key))
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def _write_single_sheet(self, file_path: Path):
        """Escribe Excel con una sola hoja."""
        all_data = []
        for data in self._accumulated_data.values():
            all_data.extend(data)
        
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_excel(str(file_path), index=False)
    
    def _write_txt(self, file_path: Path):
        """Escribe archivo TXT consolidado."""
        all_data = []
        for data in self._accumulated_data.values():
            all_data.extend(data)
        
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_string(str(file_path), index=False)
    
    def _sanitize_sheet_name(self, name: str) -> str:
        """Limpia nombre de hoja de Excel."""
        # Max 31 caracteres, sin caracteres especiales
        name = name[:31]
        for char in ['/', '\\', '*', '[', ']', ':', '?']:
            name = name.replace(char, '-')
        return name
    
    def _open_file(self, file_path: Path):
        """Abre el archivo Excel generado."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(str(file_path))
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{file_path}"')
        except Exception as e:
            logger.warning(f"No se pudo abrir el archivo automáticamente: {e}")

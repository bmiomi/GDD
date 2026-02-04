"""
Módulo Server - Consultas y gestión de servidor XSales.
"""
from plugins.xsales.src.modules.base_module import XSalesModule, ModuleMetadata
from plugins.xsales.src.modules.module_registry import ModuleRegistry
from plugins.xsales.src.modules.Server.config import ConfigServer
from typing import Any


@ModuleRegistry.register
class ServerModule(XSalesModule):
    """
    Módulo para consultas al servidor XSales.
    
    Funcionalidades:
    - Consultas SQL a base de datos XSales
    - Validación de clientes
    - Reportes de pedidos
    - Revisiones de madrugada
    """
    
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="server",
            display_name="Server - Consultas XSales",
            description="Consultas y reportes del servidor XSales",
            version="1.0.0"
        )
    
    def __init__(self):
        """Constructor del módulo Server"""
        super().__init__()
        self._config = ConfigServer()
        self._config.Revisiones = 'Server'
        self.validadorsql = None
        self.contenedor = []
        self.contador = 0
        self.datos_por_turno = {}  # {turno: [(nombredz, dataset), ...]}
    
    def setup(self, context) -> bool:
        """Inicialización del módulo Server"""
        super().setup(context)
        return True
    
    def run(self, context) -> Any:
        """Ejecución principal del módulo Server"""
        from plugins.xsales.inputquestion import preguntass
        
        # Realizar preguntas específicas de Server
        self.dato = preguntass(
            context.questionary,
            self._config
        )
        
        # Mostrar información
        self.mostrar_info(
            self.dato.ContenedorDZ,
            context.console
        )
        
        # Generar archivo si se solicitó
        self.generararchivo(
            self.dato.reporte,
            self.dato.Opcion,
            self.dato.Turno,
            context.console
        )
        
        return {"status": "success", "data": self.dato}
    
    def mostrar_info(self, nombresdz, console):
        """Procesa consultas para distribuidores"""
        from plugins.xsales.src.modules.Server.Pagedriver.xsalesbeta import Xsales
        
        with console.status('Procesando..', spinner=self._config.spinner):
            for nombredz in nombresdz:
                # Crear instancia de Xsales para cada distribuidor
                xsales = Xsales(name=nombredz)
                self.consulta_Basedatos(nombredz, xsales, console)
    
    def consulta_Basedatos(self, nombredz, xsales, console):
        """Ejecuta consulta a base de datos"""
        from plugins.xsales.src.modules.Server.User.validador import ValidatorSql
        from plugins.xsales.src.modules.Server.User.Consultas import consultas
        import traceback
        
        try:
            # Validar que xsales se inicializó correctamente
            if not hasattr(xsales, 'estado'):
                console.log(f"[red]⚠ {nombredz}: Xsales no tiene atributo 'estado'")
                return
            
            if not xsales.estado:
                console.log(f"[yellow]⚠ {nombredz}: Sesión XSales no activa (estado=False)")
                return
            
            # Configurar distribuidor
            consultas.NDISTRIBUIDOR = xsales.name
            
            # Generar SQL - capturar error aquí específicamente
            try:
                # Usar la estructura correcta para consultas
                sql_config = self._config.configConsultasStructured
                if not sql_config:
                    console.log(f"[red]⚠ {nombredz}: No hay configuración de consultas")
                    return
                
                # Limpiar la opción de espacios en blanco
                opcion_limpia = str(self.dato.Opcion).strip()
                
                # Normalizar: convertir a mayúsculas y eliminar espacios
                opcion_normalizada = opcion_limpia.upper().strip()
                
                # Buscar en las claves disponibles
                claves_disponibles = {k.upper(): k for k in sql_config.keys()}
                
                if opcion_normalizada not in claves_disponibles:
                    console.log(f"[red]✗ {nombredz}: Opción no encontrada: '{opcion_normalizada}'")
                    console.log(f"[red]  → Claves disponibles: {list(sql_config.keys())}")
                    return
                
                # Obtener la clave correcta
                clave_real = claves_disponibles[opcion_normalizada]
                
                # Construir diccionario de todos los parámetros (usuario + sistema)
                todos_parametros = dict(self.dato.parametros_usuario or {})
                todos_parametros['NDISTRIBUIDOR'] = xsales.name
                
                # Inyectar parámetros en consultas antes de generar SQL
                for param_name, param_value in todos_parametros.items():
                    if isinstance(param_value, str):
                        param_value = param_value.strip()
                    setattr(consultas, param_name, param_value)
                
                # Llamar a consultas.consulta con la estructura correcta
                sql_callable = consultas.consulta(
                    clave_real,
                    sql_config
                )
                
                if not callable(sql_callable):
                    console.log(f"[red]⚠ {nombredz}: consulta() no retornó callable para opción '{clave_real}'")
                    return
                
                sql = sql_callable()
                if not sql:
                    console.log(f"[red]⚠ {nombredz}: SQL generado está vacío")
                    return
                
                # 🔍 MOSTRAR SQL GENERADO (para debugging)
                console.log(f"[cyan]📋 SQL para {nombredz}:[/cyan]")
                console.log(f"[yellow]{sql[:500]}...[/yellow]" if len(sql) > 500 else f"[yellow]{sql}[/yellow]")
                    
            except KeyError as ke:
                console.log(f"[red]✗ {nombredz}: KeyError: {ke}")
                console.log(f"[red]  → Claves disponibles: {list(sql_config.keys()) if sql_config else 'ninguna'}")
                return
            except Exception as sql_err:
                console.log(f"[red]✗ {nombredz}: Error generando SQL: {sql_err}")
                return
            
            # Ejecutar consulta
            result = xsales.consultar(sql)
            print("result de consulta:", result)
            dataset = None
            
            # Verificar si hay respuesta JSON del API
            if getattr(xsales, 'use_query_api', False) and xsales.xsalesresponse_json:
                response = xsales.xsalesresponse_json
                
                # Verificar errores en la respuesta
                message_type = response.get('MessageType')
                message = response.get('Message', '')
                
                # MessageType 69 indica error
                if message_type == 69:
                    error_msg = message
                    
                    # Intentar obtener mensaje más específico de QueryInfResult
                    data = response.get('Data')
                    if isinstance(data, dict):
                        query_inf = data.get('QueryInfResult')
                        if isinstance(query_inf, list) and query_inf:
                            error_msg = query_inf[0].get('Msg', message)
                    
                    console.log(f"[red]✗ {nombredz}: {error_msg}")
                    return
                
                # Extraer datos si no hay error
                data = response.get('Data') if isinstance(response, dict) else None
                if isinstance(data, list):
                    dataset = data
                elif isinstance(data, dict):
                    result = data.get('Result') or data.get('result') or data.get('data')
                    if isinstance(result, list):
                        dataset = result
            elif isinstance(result, list):
                dataset = result

            if dataset:
                # Agregar columna de Distribuidor a cada fila
                for row in dataset:
                    if isinstance(row, dict):
                        row['Distribuidor'] = nombredz
                
                # Guardar datos agrupados por turno
                turno = self.dato.Turno if hasattr(self, 'dato') else 'Sin Turno'
                if turno not in self.datos_por_turno:
                    self.datos_por_turno[turno] = []
                self.datos_por_turno[turno].extend(dataset)
                
                self.contenedor.append(dataset[0])
                self.validadorsql = ValidatorSql(clave_real, dataset)
                console.log(f"[green]✓ Revisión completada para {nombredz}")
            else:
                console.log(f"[yellow]⚠ {nombredz}: Resultado vacío de la consulta")
                
        except Warning as e:
            console.log(f"[yellow]⚠ {nombredz}: {e}")
        except ValueError as e:
            console.log(f"[red]✗ Error en {nombredz}: {e}")
        except BaseException as e:
            error_trace = traceback.format_exc()
            console.log(f"[red]✗ Error en {nombredz}: {e}")
            console.log(f"[red]{error_trace}")
    
    def generararchivo(self, respuesta, nombre: str, turno: str, console):
        """Genera archivo Excel con los resultados agrupados por turno"""
        if respuesta:
            # Verificar que existan datos para generar
            if not self.datos_por_turno:
                console.print('[yellow]⚠ No hay datos para generar el archivo.')
                return
            
            try:
                from plugins.xsales.src.modules.Server.User.validador import ValidatorSql
                archivo = self._config.path.join(self._config.folderMadrugada(), f'{nombre}')
                
                # Crear Excel con hojas por turno
                self._config.excelfile().create_file_by_sheets(archivo, self.datos_por_turno)
                console.print(f'[green]✓ Archivo generado: {archivo}.xlsx')
                
                # Limpiar datos completos (reiniciar dict en lugar de eliminar)
                self.datos_por_turno = {}
                if hasattr(ValidatorSql, 'DZCOMPLETO'):
                    ValidatorSql.DZCOMPLETO = []
            except Exception as e:
                import traceback
                console.print(f'[red]✗ Error al generar archivo: {e}')
                console.print(f'[red]{traceback.format_exc()}')
    
    def cleanup(self) -> None:
        """Limpieza del módulo Server"""
        # No hay sesión HTTP que cerrar porque Xsales se instancia en cada ejecución
        pass

"""
Ejemplo: Cómo cada módulo usa el sistema de preguntas compartidas.
"""

# ============================================
# EJEMPLO 1: FTP Module - Usa preguntas básicas
# ============================================
class FtpModule(XSalesModule):
    def run(self, context):
        from ..questions import CommonQuestions
        
        # Flujo básico estándar
        data = CommonQuestions.ask_basic_flow(
            context.questionary,
            turnos=self.config.Turnos,
            procesos=self.config.Revisiones,  # ["Validar DESC", "Validar Maestros"]
            distribuidores=self.config.Dz({'Opcion': 'TODOS'})
        )
        
        # Usar datos
        console.log(f"Turno: {data.turno}")
        console.log(f"Proceso: {data.opcion}")
        console.log(f"Distribuidores: {data.distribuidores}")
        
        if data.generar_reporte:
            self.generar_reporte()


# ============================================
# EJEMPLO 2: Server Module - Usa preguntas básicas (igual que FTP)
# ============================================
class ServerModule(XSalesModule):
    def run(self, context):
        from ..questions import CommonQuestions
        
        # MISMO flujo que FTP, pero con config diferente
        data = CommonQuestions.ask_basic_flow(
            context.questionary,
            turnos=self.config.Turnos,
            procesos=self.config.Revisiones,  # ["Pedidos", "Revisiones Matutinas"]
            distribuidores=self.config.Dz({'Opcion': 'TODOS'})
        )
        
        # Las preguntas son iguales, pero las opciones vienen de su Config


# ============================================
# EJEMPLO 3: Status Module - Preguntas personalizadas con Builder
# ============================================
class StatusModule(XSalesModule):
    def run(self, context):
        from ..questions import QuestionBuilder
        
        # Flujo personalizado
        builder = QuestionBuilder(context.questionary)
        data, custom = (builder
            .ask_turno(self.config.Turnos)
            # Status NO pregunta proceso, solo monitorea
            .ask_distribuidores(
                self.config.Dz({'Opcion': 'TODOS'}),
                mensaje="¿Qué distribuidores monitorear?"
            )
            .ask_custom(
                'intervalo',
                '¿Cada cuánto actualizar?',
                ['5 segundos', '10 segundos', '30 segundos']
            )
            .ask_reporte(mensaje='¿Generar log del monitoreo?')
            .build())
        
        # Acceder a datos
        intervalo = custom['intervalo']


# ============================================
# EJEMPLO 4: Nuevo módulo con flujo condicional
# ============================================
class ReportesModule(XSalesModule):
    def run(self, context):
        from ..questions import QuestionBuilder
        
        builder = QuestionBuilder(context.questionary)
        data, custom = (builder
            .ask_turno(self.config.Turnos)
            .ask_proceso(self.config.Revisiones)
            .ask_custom(
                'tipo_reporte',
                '¿Tipo de reporte?',
                ['Consolidado', 'Por distribuidor']
            )
            # Pregunta condicional
            .ask_if(
                custom.get('tipo_reporte') == 'Por distribuidor',
                lambda b: b.ask_distribuidores(self.config.Dz())
            )
            .ask_confirm('incluir_graficos', '¿Incluir gráficos?')
            .build())

"""Constructor de consultas SQL para XSales."""
from datetime import date, timedelta

ahora = date.today()
ayer = ahora - timedelta(days=2) if ahora.weekday() == 0 else ahora - timedelta(days=1)


class consultas:
    NDISTRIBUIDOR = None

    @classmethod
    def consulta(cls, nombrerevicion: str, config: dict):
        """Retorna un callable que genera el SQL para la revisión indicada."""
        revisiones = config.get(nombrerevicion) if isinstance(config, dict) else None
        if not isinstance(revisiones, dict):
            return lambda: ""
        return lambda: cls.obtener_consulta(revisiones)
<<<<<<< HEAD

    @classmethod
    def obtener_consulta(cls, revision: dict) -> str:
        consulta_sql = revision.get('sql')
        parametros = revision.get('parametros', [])

        if isinstance(consulta_sql, dict) and 'if' in consulta_sql:
            # Manejo de distribuidores
            if 'distribuidores' in consulta_sql:
                distribuidores = consulta_sql.get('distribuidores') or {}
                nd = (cls.NDISTRIBUIDOR or '').lower()
                if nd in distribuidores:
                    sql = consulta_sql.get('then', '')
                    for key in parametros:
                        if key == 'ayer':
                            sql = sql.replace(f'{{{{{key}}}}}', str(ayer))
                        elif key == 'NDISTRIBUIDOR':
                            sql = sql.replace(f'{{{{{key}}}}}', distribuidores[nd])
                    return sql

            # Evaluar condición
            condition = consulta_sql.get('if', '')
            for key in parametros:
                if key == 'NDISTRIBUIDOR':
                    condition = condition.replace(f'{{{{{key}}}}}', f"'{str(cls.NDISTRIBUIDOR)}'")
                elif key == 'ayer':
                    condition = condition.replace(f'{{{{{key}}}}}', str(ayer))

            if condition and eval(condition):
                return consulta_sql.get('then', '')
            return consulta_sql.get('else', '')

        if isinstance(consulta_sql, str):
            sql = consulta_sql
            for key in parametros:
                if key == 'ayer':
                    sql = sql.replace(f'{{{{{key}}}}}', str(ayer))
                elif key == 'NDISTRIBUIDOR':
                    sql = sql.replace(f'{{{{{key}}}}}', f"'{str(cls.NDISTRIBUIDOR)}'")
            return sql

=======

    @classmethod
    def obtener_consulta(cls, revision: dict) -> str:
        consulta_sql = revision.get('sql')
        
        # Combinar parámetros de usuario y sistema
        parametros_usuario = revision.get('parametros_usuario', [])
        parametros_sistema = revision.get('parametros_sistema', [])
        parametros = parametros_usuario + parametros_sistema

        if isinstance(consulta_sql, dict) and 'if' in consulta_sql:
            # Manejo de distribuidores
            if 'distribuidores' in consulta_sql:
                distribuidores = consulta_sql.get('distribuidores') or {}
                nd = (cls.NDISTRIBUIDOR or '').lower()
                if nd in distribuidores:
                    sql = consulta_sql.get('then', '')
                    for key in parametros:
                        if key == 'ayer':
                            sql = sql.replace(f'{{{{{key}}}}}', str(ayer))
                        elif key == 'NDISTRIBUIDOR':
                            sql = sql.replace(f'{{{{{key}}}}}', distribuidores[nd])
                        else:
                            # Parámetro de usuario dinámico
                            valor = getattr(cls, key, None)
                            if valor is not None:
                                sql = sql.replace(f'{{{{{key}}}}}', str(valor))
                    return sql

            # Evaluar condición
            condition = consulta_sql.get('if', '')
            for key in parametros:
                if key == 'NDISTRIBUIDOR':
                    condition = condition.replace(f'{{{{{key}}}}}', f"'{str(cls.NDISTRIBUIDOR)}'")
                elif key == 'ayer':
                    condition = condition.replace(f'{{{{{key}}}}}', str(ayer))
                else:
                    # Parámetro de usuario dinámico
                    valor = getattr(cls, key, None)
                    if valor is not None:
                        condition = condition.replace(f'{{{{{key}}}}}', f"'{str(valor)}'")

            if condition and eval(condition):
                return consulta_sql.get('then', '')
            return consulta_sql.get('else', '')

        if isinstance(consulta_sql, str):
            sql = consulta_sql
            for key in parametros:
                if key == 'ayer':
                    sql = sql.replace(f'{{{{{key}}}}}', str(ayer))
                elif key == 'NDISTRIBUIDOR':
                    sql = sql.replace(f'{{{{{key}}}}}', f"'{str(cls.NDISTRIBUIDOR)}'")
                else:
                    # Parámetro de usuario dinámico
                    valor = getattr(cls, key, None)
                    if valor is not None:
                        sql = sql.replace(f'{{{{{key}}}}}', str(valor))
            return sql

>>>>>>> revision
        return ""

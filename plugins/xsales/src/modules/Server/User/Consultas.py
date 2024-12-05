#alicia albornos
from datetime import date, timedelta

ahora = date.today()
ayer = ahora -timedelta(days=2) if ahora.weekday() == 0  else ahora -timedelta(days=1)

class consultas:

    NDISTRIBUIDOR=None;


    @classmethod
    def consulta_beta(cls,dato,nombrerevicion,config):      
        for key in config.keys():
            if key == dato:
                return cls.retornar_Sentencia_sql(config[key],nombrerevicion)
            
    @classmethod
    def retornar_Sentencia_sql(cls,revisiones:dict,nombrerevicion:str):
        return cls.obtener_consulta(revisiones,nombrerevicion)

    @classmethod
    def obtener_consulta(cls,revisiones:dict,nombrerevicion:str):
        consulta_sql=revisiones[nombrerevicion]['sql']
        parametros =revisiones[nombrerevicion]['parametros'] 
        if 'if' in consulta_sql:
            if 'distribuidores' in consulta_sql:
                distribuidores=consulta_sql.get('distribuidores')
                for key in distribuidores:
                    if key == cls.NDISTRIBUIDOR:
                       for key in parametros:
                        sql=consulta_sql['then'].replace(f'{{{{{key}}}}}',str(ayer)) 
                        if key=='NDISTRIBUIDOR':
                            sql=sql.replace(f'{{{{{key}}}}}',distribuidores[cls.NDISTRIBUIDOR]) 
                return sql
            
            for key in parametros:
                parametro=consulta_sql['if'].replace(f'{{{{{key}}}}}', f"'{str(cls.NDISTRIBUIDOR)}'")

            if eval(parametro):
                return consulta_sql['then']
            return consulta_sql['else']
        
        if revisiones.get(nombrerevicion).get('sql'):
            for key in parametros:
                valor=consulta_sql.replace(f'{{{{{key}}}}}','0952461093')
 
            return valor

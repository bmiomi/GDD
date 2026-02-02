from datetime import date, timedelta, datetime
from enum import Enum
from typing import Dict, List, Optional

class HorasenvioStock(Enum):

    horaDiurnodz='11:59:00 AM'

    horaNocturnodz='11:59:00 PM'

class ValidatorSql:

    DZCOMPLETO=[]

    def __init__(self, tipoconsulta: str, dataset: List[dict]):
        self.__dataset = dataset
        self.validador = self.validar(tipoconsulta)

    def validar(self,tipoconsulta:str)->Optional[List[Dict]]:

        contenedor = {
            'REVICION_MADRUGADA': self.vmatutina,
            'DESC.DIURNOS': self.descuentosDiurnos,
            'Total_Pedidos': self.validartotalpedidos,
            'VALIDAR_ClIENTE':self.general
        }
        funcion = contenedor.get(tipoconsulta, 0)
        if not funcion:
            print(f'No se reconoce el tipo de consulta {funcion}')
            return {}

        if funcion():
            ValidatorSql.DZCOMPLETO.append(self.__dataset)
            return self.__dataset
    
    def vmatutina(self) -> bool:        
        #TODO
        #revisar este proceso
        "valida informacion de revisiones matutinas"
        waringistemporales = []
        for i in self.__dataset:
            for x in i:
                valor = i[x]
                if x.startswith('preventa') and valor != date.today().strftime('%d/%m/%Y'):
                    raise ValueError(f'[ERROR] {valor} con preventa {valor} ')
                if 'inicio' in x.lower():
                    hora_stock = valor
                    if isinstance(valor, str) and 'T' in valor:
                        try:
                            hora_stock = valor.split('T', 1)[1].split('.', 1)[0]
                        except Exception:
                            hora_stock = valor
                    self._calcularstock(x, hora_stock)
                if valor == 0 and not x.lower().endswith('_today'):
                    waringistemporales.append(valor)
                            
        if len(waringistemporales) >= 1:
            raise Warning(f"[Warnnig] No se tiene datos para  {waringistemporales} ")
        return True

    def _parse_time_only(self, valor_hora: str) -> Optional[datetime]:
        if not isinstance(valor_hora, str) or not valor_hora.strip():
            return None
        valor = valor_hora.strip()

        try:
            return datetime.fromisoformat(valor.replace('Z', ''))
        except Exception:
            pass

        if 'T' in valor:
            try:
                fecha, hora = valor.split('T', 1)
                hora = hora.split('.')[0]
                return datetime.fromisoformat(f"{fecha}T{hora}")
            except Exception:
                pass

        try:
            parse_val = valor.replace('p. m.', 'PM') if 'p. m.' in valor else valor.replace('a. m.', 'AM')
            return datetime.strptime(parse_val, '%d/%m/%Y %I:%M:%S %p')
        except Exception:
            pass

        try:
            return datetime.strptime(valor, '%H:%M:%S')
        except Exception:
            return None

    def _calcularstock(self, clave_hora: str, valor_Hora_stock: str) -> bool:
        """ 
        si la fecha  obtenida de la consulta no es la actual  y la hora es es menor return TRUE 
        si la fecha  obtenida en la consulta es la actual  y la hora es es menor  return TRUE
        '18/9/2022 10:16:37 a. m.'
        """        
        hoy = date.today()
        ayer = hoy-timedelta(days=1)

        parsed = self._parse_time_only(valor_Hora_stock)
        if not parsed:
            return True

        fhora = parsed.time()
        ffecha = parsed.date() if parsed.date() else None
        hora_diurna = datetime.strptime(HorasenvioStock.horaDiurnodz.value, '%I:%M:%S %p').time()
        hora_nocturna = datetime.strptime(HorasenvioStock.horaNocturnodz.value, '%I:%M:%S %p').time()

        if clave_hora == 'HoraECUInicioStock' and ffecha:
            if (ffecha != hoy and fhora >= hora_nocturna) or (ffecha == hoy and fhora >= hora_diurna):
                raise Warning(
                    f"[ERROR-DZ] stock fuera de horario {valor_Hora_stock}  ")

        if clave_hora == 'HoraECUInicioStock' and not ffecha:
            if (fhora.hour >= 12 and fhora >= hora_nocturna) or (fhora.hour < 12 and fhora >= hora_diurna):
                raise Warning(
                    f"[ERROR-DZ] stock fuera de horario {valor_Hora_stock}  ")

        if clave_hora == 'HoraECUInicioStock' and (hoy != ayer and datetime.strptime('10:00:00 PM', '%I:%M:%S %p').time() <= fhora):
            raise Warning(
                f"[ERROR-DIRECTA] stock fuera de horario  para {valor_Hora_stock} "
            )
        return True

    def validartotalpedidos(self):

        for i in self.__dataset:
            if i['DMD_PROCESADOS'] == i['ERP_EXITO'] == i['DMD_TOTAL']:
                return f"[successful] informacion esta cuadrada DMD_TOTAL: {i['DMD_TOTAL']} "
            if i['DMD_EXTENDIDAS'] != 0 and i['DMD_TRANSITO'] != 0 and i['DMD_NOPROCESADOS'] != 0:
                raise Warning( f"[Warrning] se tiene informacion por procesar: ") 
            if i['DMD_ERROR'] != 0 or i['DMD_ERRSOAP'] != 0:
                raise ValueError("[ERROR] se tiene informacion en DMD_ERROR / DMD_ERRSOAP: ")

    def descuentosDiurnos(self):
        return True

    def vdnocturnos(self):
        "valida informacion de revision de descuentos nocturnos."

        "data: list[dict]"

        d = {

            'REGIONAL/DISTRIBUIDOR': 'disanahisa',
            'DIDCODE': '2503230000663',
            'CLIENTE': '300003938',
            'FECHA': '2021/10/27 15:32:44.000',
            'RUTA': '250',
            'PORCENTAJE': '16.0',
            'STATUS': 'Aprobado',
            'PROCESADO': 'No',
            'APVCODE': 'nan'
        }

    def general(self):

        for i in self.__dataset:
            for x , v in i.items():
                print(f"{x}: {v}",end=' ')

        return True

import time
import base64
from typing import Dict, List, Tuple
from rich.live import Live
from rich.table import Table
from rich import box


from plugins.xsales.src.modules.Status.config import ConfigStatus


class Status:

    config=ConfigStatus()

    def __init__(self):

        self.dzincompletos:List[Dict]=[] #incremental
        self.dzcompletos:list=[]

    @property
    def estado(self):
        return True if len(self.dzincompletos)==23 else False
    
    def obtener_peticion(self,DZ):
        from requests_html import HTMLSession

        request_=HTMLSession()
        credenciales=f"Data Source=USAWS2012404;Initial Catalog={DZ.upper()}_XSS_441_PRD;User Id={DZ.upper()};Password=XSales.{DZ.upper()}@2015;"
        base64_message=base64.b64encode(credenciales.encode('ascii')).decode('ascii')
        solicitud=f"http://prd1.xsalesmobile.net/{DZ}/xsc/rep/inner/ExportXMLRep.asmx/StatusRoute?ConnectionString={base64_message}&rotCode=&statusFilter=&partialStatusFilter="
       
        req=request_.get(solicitud)
        if req.status_code==200:
            return req
        raise BaseException('Direccion no valida')

    def statusrutas(self,DZ:str)->Tuple:
        import json
        import xmltodict

        try:
            bajada=[]
            parcial=[]
            dies=[]
            total=[]
            req=self.obtener_peticion(DZ)
            respo=xmltodict.parse(req.content,encoding='utf-8')
            respon=json.loads(json.dumps(respo))
            for i in respon.get('ArrayOfStatusRoute').get('StatusRoute'):
                if i['status']== '3' and  self.config.fecha in i['statusDate'] :
                    bajada.append(i['rotCode'])
                if i['partialStatus'] in ('7','8') and  self.config.fecha in i['statusDate']:
                    parcial.append(i['rotCode'])
                if i['status']=='11' and  self.config.fecha in i['statusDate']:
                    total.append(i['rotCode'])
                if i['status']=='10' and  self.config.fecha in i['statusDate']:
                    dies.append(i['rotCode'])
            return (bajada,parcial,dies,total)
        except BaseException as e:
            raise BaseException(f'{e}')

    def validardz(self,listadodz):
        print('entre: ')

        for i in listadodz:
            
            bajada,parcial,dies,Total=self.statusrutas(i)

            statusDz={

                'name':i,
                'status':
                    { 'bajada':bajada,
                        'parcial':parcial,
                        'dies':dies,
                        'Total':Total
                    }
            }

            if len(statusDz['status']['bajada'])!=0: #estado total
                self.dzincompletos.append(statusDz)

    def generar_table(self ):
       
        numero=1
        self.table=Table(box=box.ROUNDED)
        self.table.add_column('Nombre')
        self.table.add_column('bajada')
        self.table.add_column('Parcial')
        self.table.add_column('dies')
        self.table.add_column('Total')

        for i in self.dzincompletos:
            estado=i['status']
            self.table.add_row(i['name'],str(estado['bajada']),str(estado['parcial']),str(estado['dies']),str(estado['Total']),style=f"color({numero})")
            numero+=1
        return self.table
   
    def mostrar_info(self,namedz,):
        try:

            self.validardz(namedz)

            with Live (self.generar_table()) as live:
                while self.estado:
                    time.sleep(5)
                    print('reiniciar tabla')
                    self.dzincompletos=[]
                    self.validardz(namedz)
                    live.update(self.generar_table())

        except ValueError as e:
            print( f'FINALIZDO: {e}' )
        except KeyboardInterrupt:
            print('se cerrarron las solicitudes.')

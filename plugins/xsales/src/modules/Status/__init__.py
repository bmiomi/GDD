from typing import List,Tuple,Dict
from unicodedata import name
from rich.table import Table
from rich.live import Live

class Status:

    contador=0
  
    def __init__(self,dato,config):

        self.config=config
        self.dato=dato
        self.dz:List=list(self.config.Dz()) #decremental 
        self.dzincompletos:List[Dict]=[] #incremental
        self.dzcompletos:list=[]

    def leer_archivo(self) -> List:

        "Crea un archivo de texto en caso de no exitir y retorna los dz que han culminado \
         su sincronizacion total en una lista"        

        diractual=f'{self.config.filestatus}dzTotal-{self.config.fecha}'
        
        if self.config.path.isfile(diractual):
            self.dzcompletos=[i.replace('\n','') for i in  open(diractual,'r+').readlines()]
    
    def agregar_archivo(self,name:dict):
        with open(f'{self.config.filestatus}dzTotal-{self.config.fecha}','a') as dz: 
            dz.writelines( f"{name}\n" )
   
    def retornardz(self,nombre)-> str:

        self.leer_archivo()

        if len(self.dzcompletos)==23:
            raise ValueError('No existen DZ que validar')            

        if nombre !='':
            return [nombre]

        return [i for i in self.dz if i not in self.dzcompletos]

    def statusrutas(self,DZ:str)->Tuple:
        import base64
        import json
        import xmltodict
        from requests_html import HTMLSession 

        bajada=[]
        parcial=[]
        dies=[]
        total=[]
        request_=HTMLSession()
        credenciales=f"Data Source=USAWS2012404;Initial Catalog={DZ.upper()}_XSS_441_PRD;User Id={DZ.upper()};Password=XSales.{DZ.upper()}@2015;"
        base64_message=base64.b64encode(credenciales.encode('ascii')).decode('ascii')
        solicitud=f"http://prd1.xsalesmobile.net/{DZ}/xsc/rep/inner/ExportXMLRep.asmx/StatusRoute?ConnectionString={base64_message}&rotCode=&statusFilter=&partialStatusFilter="
        req=request_.get(solicitud)
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
        
    def buscardz(self,name)-> bool:

        return any( filter(lambda dz:  dz['name']== name,self.dzincompletos  )  )

    def validardz(self,nameDz):
       
        if not self.buscardz(nameDz) and nameDz != 'PRONACA': # dz no existe
            bajada,parcial,dies,Total=self.statusrutas(nameDz)
            statusDz={

                'name':nameDz,
                'status':                    
                    { 'bajada':bajada,
                      'parcial':parcial,
                      'dies':dies,
                      'Total':Total
                    }                
            }

            if len(statusDz['status']['bajada'])==0:#estado total
                self.agregar_archivo(statusDz['name'])

            self.dzincompletos.append(statusDz)

    def mostrar_info(self):

        try:

            DzFaltantes=self.retornardz(self.dato.Opcion)

            for name in DzFaltantes:
                self.validardz(name)

            with Live (self.generar_table(),refresh_per_second=4) as live:
                for _ in self.dzincompletos:
                    live.update(self.generar_table())
   
        except ValueError as e:
            print( f'FINALIZDO: {e}' )
        except KeyboardInterrupt:
            print('se cerrarron las solicitudes.')

    def generar_table(self):
        numero=1
        self.table=Table(title='STATUS RUTAS DZ ')
        self.table.add_column('NOMBRE')
        self.table.add_column('bajada')
        self.table.add_column('Parcial')
        self.table.add_column('dies')
        self.table.add_column('Total')
    
        for i in self.dzincompletos:

            nombre=i['name']
            estado=i['status']
            bajada=estado['bajada']
            parcial=estado['parcial']
            dies=estado['dies']
            total=estado['Total']

            self.table.add_row(nombre,str(bajada),str(parcial),str(dies),str(total),style=f"color({numero})")
            numero+=1

        return self.table

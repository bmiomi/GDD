# from typing import List,Tuple,Dict
# from rich.table import Table
# from rich.live import Live
# from plugins.xsales.src.config import Config

# class Status:

#     contador=0
#     config=Config()
  
#     def __init__(self):

#         self.fecha=self.config.fecha()
#         self.status_:List[Dict]=[] #incremental
#         self.dz=list(self.config.Dz()) #decremental 

#     def mapdz(self) -> List:

#         "Crea un archivo de texto en caso de no exitir y retorna los dz que han culminado su sincronizacion total en una lista"        
#         diractual=f'dzTotal-{self.fecha}'
#         if self.config.path.isfile(diractual) :
#             with open(diractual,'r+') as _file:   
#                 return [i.replace('\n','') for i in  _file.readlines()]
#         return []

#     def retornardz(self)-> str:
#         import random
#         infile=self.mapdz()
#         if len(infile)==23:
#             raise ValueError('No existen DZ que validar')

#         self.dz=[i for i in self.dz if i not in infile]
#         self.contador=len(self.dz)
#         return random.choice( self.dz )

#     def buscardz(self,name)-> bool:
#         return any( filter(lambda dz:  dz['name']== name,self.status_  )  )

#     def statusrutas(self,DZ:str)->Tuple:

#         import base64
#         import json
#         import xmltodict
#         from requests_html import HTMLSession 

#         bajada=[]
#         parcial=[]
#         total=[]
#         request_=HTMLSession()

#         credenciales=f"Data Source=USAWS2012404;Initial Catalog={DZ.upper()}_XSS_441_PRD;User Id={DZ.upper()};Password=XSales.{DZ.upper()}@2015;"
#         base64_message=base64.b64encode(credenciales.encode('ascii')).decode('ascii')
#         solicitud=f"http://prd1.xsalesmobile.net/{DZ}/xsc/rep/inner/ExportXMLRep.asmx/StatusRoute?ConnectionString={base64_message}&rotCode=&statusFilter=&partialStatusFilter="
#         req=request_.get(solicitud)
#         respo=xmltodict.parse(req.content,encoding='utf-8')
#         respon=json.loads(json.dumps(respo))    
#         for i in respon.get('ArrayOfStatusRoute').get('StatusRoute'):
#             if i['status']=='3' and  self.fecha in i['statusDate'] :
#                 bajada.append(i['rotCode'])
#             if i['partialStatus'] in ('7','8') and  self.fecha in i['statusDate']: 
#                 parcial.append(i['rotCode'])
#             if i['status']=='11' and  self.fecha in i['statusDate']:
#                 total.append(i['rotCode'])
#         return (bajada,parcial,total)

#     def validardz(self,nameDz):

#         if not self.buscardz(nameDz) and nameDz != 'PRONACA': # dz no existe

#             name={}
#             name['name']=nameDz
#             name['status']=[]    
#             status={}
#             status['bajada'],status['parcial'],status['Total']=self.statusrutas(nameDz)

#             self.estado(status,nameDz)

#             name['status'].append(status)
#             self.status_.append(name)

#     def estado(self,status:dict,a:str):

#         if len(status['bajada'])==0:#estado total
#             with open(f'dzTotal-{self.fecha}','a') as dz: 
#                 # print(f"\033[33m Todas las rutas para {a} se encuentran sincronizadas \033[00m")
#                 dz.writelines( f"{a}\n" )
        
#     def txs(self):

#         import os
#         try:
#             # cont=0
#             while len(self.dz)>=1:
#                 a=self.retornardz()
#                 self.validardz(a)

#                 if self.contador== len(self.status_)+1:                    

#                     with Live (self.generar_table(),refresh_per_second=4) as live:
#                         for _ in self.status_:
#                             live.update(self.generar_table())
   
#                     input('precione enter para volver a realizar las consultas... ')
#                     self.status_=[]
#                     os.system('cls')
                    
#                     # cont+=1
#                     # time.sleep(5+cont)
#         except ValueError as e:
#             print( f'FINALIZDO: {e}' )
#         except KeyboardInterrupt:
#             print('se cerrarron las solicitudes.')
#                 os.system('cls')

#     def generar_table(self):
#         numero=1
#         self.table=Table(title='STATUS RUTAS DZ')
#         self.table.add_column('NOMBRE')
#         self.table.add_column('bajada')
#         self.table.add_column('Parcial')
#         self.table.add_column('Total')
    
#         for i in self.status_:
#             nombre=i['name']
#             estado=i['status'][0]
#             bajada=estado['bajada']
#             parcial=estado['parcial']
#             total=estado['Total']
#             self.table.add_row(nombre,str(bajada),str(parcial),str(total),style=f"color({numero})")
#             numero+=1
#         return self.table

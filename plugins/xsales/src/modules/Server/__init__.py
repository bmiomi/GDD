from typing import Dict, List
from .Pagedriver.xsalesbeta import  Xsales
from .User.validador import ValidatorSql
from .User.Consultas import consultas

class  Page(Xsales):
    
    
    def __init__(self,dato,Config) :

        """
            nombre: Nmbre del Dz que se toma para ingresar a la paguina solicitada 

        """
        self.message=[]
        self.dato=dato 
        self.Config=Config
        self.validadorsql=None


    def consulta_Basedatos(self )-> None:

        sql=self.__get_consulta(self.dato.Opcion)
        self.consultar(sql)

        if self.get_tamanio_paguinacion == 0 and self.status_table() == True:

            self.validadorsql:ValidatorSql=ValidatorSql(self.dato.Opcion,self.extraerhtml(self._config.excelfile())) 

            self.generararchivo(self.dato.Opcion,self.validadorsql.validador,self._config.excelfile())
            
        elif self.get_tamanio_paguinacion >=1:

            self.Descargar_excel(sql)

    def __get_consulta( self,opcion):

        dic_consultas={
        'DESC.NOCTURNOS':consultas.Descuentos_Nocturno,
        'Total_Pedidos':consultas.totalPedidos,
        'VALIDAR_ClIENTE':consultas.cliente,
        'DESC.DIURNOS':consultas.Descuentos_Demadrugada,
        'REVICION_MADRUGADA':consultas.revisionmadrugada
        }

        try:

            s=dic_consultas.get(opcion,0)

            if isinstance(s,int):
                return self._config.config['Consultas']['server'][opcion]
            return s()
        except TypeError:
            
            if self.dato.dato!=None and self.name!=None:
                 return dic_consultas.get(opcion)(self.dato.dato)
            return dic_consultas.get(opcion)(self.name)

    def generararchivo(self,nombre:str,data:list[dict],ExcelFile):

        namefile={'Total_Pedidos':'Dz-ReportPedidos.xlsx','DESC.DIURNOS':'NegoGdd.xlsx'}

        namefile=namefile.get(nombre,'indefinido')
        
        if namefile != 'indefinido':

           # ExcelFile._nombrearchivo=namefile
            ExcelFile.append_df_to_excel(data)
        
        if nombre == 'REVICION_MADRUGADA':
            archivo=''.join([self._config.folderMadrugada(),'REVICION_MADRUGADA'])
            ExcelFile.filetxt( namearchivo= archivo,data=data[0]) 

    def mostrar_info(self,console):

        for nombredz in self.dato.ContenedorDZ:
            super().__init__(nombredz,self.Config)
            try:
                self.consulta_Basedatos()
                console.log(f'Revisión completada para {nombredz}' )
            except Warning as e:
                console.log(f"{str(e)} DZ/Regional {nombredz}")
            except ValueError as e:
                console.log(f"{str(e)} DZ/Regional {nombredz}")
        
        if self.dato.Opcion=='DESC.DIURNOS' and len(self.dato.ContenedorDZ)==24:
          self._config.excelfile().consolidararchivo()
          print('\n se consolidara el archivo')
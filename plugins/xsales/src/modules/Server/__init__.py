
from .Pagedriver.xsalesbeta import  Xsales
from .User.validador import ValidatorSql
from .User.Consultas import consultas

#opcion hace referencia a el proceso que va a realizar ejemplo revision madrugada

class  Page(Xsales):
    
    
    def __init__(self):

        "nombre: Nmbre del Dz que se toma para ingresar a la paguina solicitada"
        super().__init__(name='Pronaca')
        self.validadorsql=None
        self.config

    def consulta_Basedatos(self )-> None:

        sql=self.__get_consulta(self.dato.Opcion)
        self.consultar(sql)

        if self.get_tamanio_paguinacion == 0 and self.status_table() == True:

            self.validadorsql:ValidatorSql=ValidatorSql(self.dato.Opcion,self.extraerhtml(self.config.excelfile())) 

            self.generararchivo(self.dato.Opcion,self.validadorsql.validador,self.config.excelfile())
            
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
                return self.config.config['Consultas']['server'][opcion]
            return s()
        except TypeError:
            
            if self.dato.dato!=None and self.name!=None:
                 return dic_consultas.get(opcion)(self.dato.dato)
            return dic_consultas.get(opcion)(self.name)

    def generararchivo(self,nombre:str,data:list[dict],ExcelFile):

        namefile={'Total_Pedidos':'Dz-ReportPedidos.xlsx','DESC.DIURNOS':'NegoGdd.xlsx'}

        namefile=namefile.get(nombre,'indefinido')
        
        if namefile != 'indefinido':

           ExcelFile._nombrearchivo=namefile
           ExcelFile.append_df_to_excel(data)
        
        if nombre == 'REVICION_MADRUGADA':
            archivo=''.join([self.config.folderMadrugada(),'REVICION_MADRUGADA'])
            ExcelFile.filetxt( namearchivo= archivo,data=data[0]) 

    def mostrar_info(self,nombredz):
        self.name=nombredz
        try:
            self.consulta_Basedatos()
            return f'Revisión completada para {nombredz}'
        except Warning as e:
            return f"{str(e)} DZ/Regional {nombredz}"
        except ValueError as e:
            return f"{str(e)} DZ/Regional {nombredz}"
        
        if self.dato.Opcion=='DESC.DIURNOS' and len(self.dato.ContenedorDZ)==24:
            self.config.excelfile().consolidararchivo()
            print('\n se consolidara el archivo')
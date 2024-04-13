from unittest.mock import Base
from .Pagedriver.xsalesbeta import  Xsales
from .User.validador import ValidatorSql
from .User.Consultas import consultas

class  Page(Xsales):
    
    def __init__(self):

        """
            nombre: Nmbre del Dz que se toma para ingresar a la paguina solicitada defecto Pronaca 

        """
        self.config.Revisiones= 'Server'
        self.validadorsql=None
        self.contenedor=[]
        self.contador=0
        
    def __get_consulta( self,opcion):
        consultas.NDISTRIBUIDOR=self.name
        dic_consultas={
        'DESC.NOCTURNOS':consultas.Descuentos_Nocturno,
        'Total_Pedidos':consultas.totalPedidos,
        'VALIDAR_ClIENTE':consultas.cliente,
        'DESC.DIURNOS':consultas.Descuentos_Demadrugada,
        'REVICION_MADRUGADA':consultas.revisionmadrugada
        }
        return dic_consultas.get(opcion,0)()
            

    def consulta_Basedatos(self )-> None:
        try:
            sql=self.__get_consulta(self.dato.Opcion)
            result=self.consulta_new_version(sql)
            self.validadorsql:ValidatorSql=ValidatorSql(self.dato.Opcion,result)
        except BaseException as e:
            print(e)
        #procesar la data en pandas
        #self.Descargar_excel(sql)
        
    def generararchivo(self,respuesta,nombre:str,console):
        if respuesta:
            archivo=self.config.path.join(self._config.folderMadrugada,f'{nombre}')
            self.config.excelfile.create_file(archivo,self.validadorsql.DZCOMPLETO)
            console.log(f'SE GENERO EL ARCHOVO EN LA RUTA {archivo}')

        
    def mostrar_info(self,nombresdz,console):
        
        with console.status('Procesando..',spinner=self.config.spinner):
            for nombredz in nombresdz:                
                try:
                    super().__init__(name=nombredz)
                    self.consulta_Basedatos()             
                    console.log( f'Revisión completada para {nombredz}')
                    self.contador+=1
                except Warning as e:
                    console.log( f"{str(e)} DZ/Regional {nombredz}")
                except ValueError as e:
                    console.log( f"{str(e)} DZ/Regional {nombredz}")

        # if self.dato.Opcion=='DESC.DIURNOS' and  self.dato.ContenedorDZ == 24:
        #     self.contenedor.append(self.validadorsql.validador)
        #     self.generararchivo(self.dato.Opcion,self.validadorsql.validador)

        # if  len(self.dato.ContenedorDZ) == self.contador:            
        #     for namefile in os.listdir(self.config.path.join( self.config.folderexcel)):
        #         # self.config.excelfile.
        #         pass
            # if self.config.path.exists( self.config.path.join( self.config.folderexcel,self.config.fecha) ):
            #     for i in os.listdir:
            #         self.generararchivo(self.nombre,i)

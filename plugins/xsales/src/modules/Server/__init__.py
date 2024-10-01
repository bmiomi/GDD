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
        return consultas.consulta(opcion)()
            
    def consulta_Basedatos(self )-> None:
        try:
            sql=self.__get_consulta(self.dato.Opcion)
            result=self.consulta_new_version(sql)
            self.validadorsql:ValidatorSql=ValidatorSql(self.dato.Opcion,result)
        except BaseException as e:
            print(e)
        
    def generararchivo(self,respuesta,nombre:str,console):
        if respuesta:
            archivo=self.config.path.join(self._config.folderMadrugada,f'{nombre}')
            self.config.excelfile.create_file(archivo,self.validadorsql.DZCOMPLETO)
            console.log(f'SE GENERO EL ARCHOVO EN LA RUTA {archivo}')
            del ValidatorSql.DZCOMPLETO

        
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

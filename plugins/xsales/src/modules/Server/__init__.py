from .Pagedriver.xsalesbeta import  Xsales
from .User.validador import ValidatorSql
from .User.Consultas import consultas
from rich.console import Console 
from rich.table import Table

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
        return consultas.consulta(opcion,self.config.configConsultas)()
            
    def consulta_Basedatos(self,nombredz,console:Console)-> None:
        try:
            if self.estado:
                sql=self.__get_consulta(self.dato.Opcion)
                result=self.consulta_new_version(sql)
                self.contenedor.append(result[0])
                self.validadorsql:ValidatorSql=ValidatorSql(self.dato.Opcion,result)
                console.log( f'Revisión completada para {nombredz}')
        except BaseException as e:
               print(e)
        except Warning as e:
                console.log( f"{str(e)} DZ/Regional {nombredz}")
        except ValueError as e:
                console.log( f"{str(e)} DZ/Regional {nombredz}")
         
        
    def generararchivo(self,respuesta,nombre:str,console):
        if respuesta:
            archivo=self.config.path.join(self._config.folderMadrugada,f'{nombre}')
            self.config.excelfile.create_file(archivo,self.validadorsql.DZCOMPLETO)
            console.prit(f'SE GENERO EL ARCHOVO EN LA RUTA {archivo}')
            del ValidatorSql.DZCOMPLETO

        
    def mostrar_info(self,nombresdz,console):        

        with console.status('Procesando..',spinner=self.config.spinner):
            for nombredz in nombresdz:                
                super().__init__(name=nombredz)
                self.consulta_Basedatos(nombredz,console)             
               


    def msd(self,console:Console):
        table=Table(title='')

        columnas = set()

        for diccionario in self.contenedor:
            columnas.update(diccionario.keys())

        print(columnas)

        for columna in columnas:
            table.add_column(columna,justify="right", style="cyan")

        for diccionario in self.contenedor:
            fila = []
            for columna in columnas:
                fila.append(str(diccionario.get(columna, "")))
            table.add_row(*fila)

        console.print(table)


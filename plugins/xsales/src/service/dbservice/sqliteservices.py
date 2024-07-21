from sqlite3 import  connect
from typing import List

class DataConn:

    """"""
    def __init__(self, db_name):
        """Constructor"""
        self.db_name = db_name

    def __enter__(self):
        """
        Open the database connection
        """
        self.conn = connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type,exc_val,exc_tb):
        """
        Close the connection
        """
        self.conn.close()
        if exc_val:
            raise f"se tiene un error de tipo {exc_val}"


    def execute_consult(self,pathfile,tablas:List,destinopath:str,namefile:str):
        result:dict={}
        listresult:list=[]

        with  DataConn(pathfile) as conn:
            for table in self.config.tablevalidacion:
                result = conn.execute(f"SELECT COUNT(*) FROM  {table} WHERE DISCODE NOT LIKE 'DES%'")
                result, =result.fetchone()
                listresult.append({{table}:{result}})
                if result == 0:
                    self.rutascero.append({'ruta':origenpath,'table':table,'result':result})

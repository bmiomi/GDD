from plugins.xsales.confi import ExcelFile
import pandas as pd

from unittest import TestCase



def test_excelfile():

    ExcelFile()

    namefile=ExcelFile._nombrearchivo    

    excel=pd.read_excel(namefile)

    df=pd.DataFrame(excel)
    
    df.to_csv(f"{namefile[:-4]}csv")

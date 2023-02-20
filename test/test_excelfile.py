from plugins.xsales.config import ExcelFile
import pandas as pd



def test_excelfile():
    namefile=ExcelFile._nombrearchivo
    
    excel=pd.read_excel(namefile)

    df=pd.DataFrame(excel)
    
    df.to_csv(f"{namefile[:-4]}csv")

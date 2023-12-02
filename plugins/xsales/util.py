<<<<<<< HEAD

from os import path,makedirs,sep,remove,listdir,scandir
=======
from os import path,makedirs,sep,scandir,listdir,remove
>>>>>>> 663323a57372b0065308c500c3a866bbc290b1f5

def createfolder(*paths):
    "Crea un directorio en caso de no existir, retorna un path"
    mipath=path.join(*paths)
    if not path.isdir(mipath):
        makedirs(mipath)
    return mipath


def descomprimir(path):
    import zipfile
    with zipfile.ZipFile(f"{path}{sep}Main.zip", "r") as zip_ref:
        zip_ref.extractall(path)


from os import path,makedirs,sep,remove,listdir,scandir

def createfolder(*paths):
    "Crea un directorio en caso de no existir, retorna un path"
    mipath=path.join(*paths)
    if not path.isdir(mipath):
        makedirs(mipath)
    return mipath


def descomprimir(path):
    import zipfile
    with zipfile.ZipFile(f"{path}\\Main.zip", "r") as zip_ref:
        zip_ref.extractall(path)

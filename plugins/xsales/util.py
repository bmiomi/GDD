
from os import makedirs,sep,scandir,listdir,remove

def createfolder(path_,*paths):
    "Crea un directorio en caso de no existir, retorna un path"
    mipath=path_.join(*paths)
    if not path_.isdir(mipath):
        makedirs(mipath)
    return mipath


def descomprimir(path):
    import zipfile
    with zipfile.ZipFile(f"{path}{sep}Main.zip", "r") as zip_ref:
        zip_ref.extractall(path)

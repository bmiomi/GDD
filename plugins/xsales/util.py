
<<<<<<< HEAD
from os import makedirs,sep,scandir,listdir,remove
=======
from os import path,makedirs,sep,remove,listdir,scandir
>>>>>>> de0a5f2993584932b82597354112f11d68d3414d

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

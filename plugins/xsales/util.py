
<<<<<<< HEAD
from os import path,makedirs,sep,remove,listdir,scandir
=======
from os import makedirs,sep,scandir,listdir,remove
>>>>>>> 6809dd0e76ee732e8887cd9e0e71a1ea12626e95

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

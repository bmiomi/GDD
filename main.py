<<<<<<< HEAD
from core.app import MyApplication
import sys

if __name__ == "__main__":
    try:
        sys.dont_write_bytecode = True
        MyApplication.run()        
    except ModuleNotFoundError as e:
        print(f"hay un error faltan dependecias por instalar {e}")
    except BaseException as e :
        print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')


=======
from core.app import MyApplication

if __name__ == "__main__":
    try:
        MyApplication.run()        
    except ModuleNotFoundError as e:
        print(f"hay un error faltan dependecias por instalar {e}")
    except BaseException as e :
        print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')



>>>>>>> 8be410330e0e34aa49b9dec88801aabcfc683771

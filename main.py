from core.app import MyApplication
import sys

if __name__ == "__main__":
    try:
        sys.dont_write_bytecode = True
        MyApplication.start()        
    except ModuleNotFoundError as e:
        print(f"hay un error faltan dependecias por instalar {e}")
    except KeyboardInterrupt:
        print('\n\n→ Programa terminado por el usuario')
    except BaseException as e:
        print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')



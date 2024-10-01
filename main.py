from core.app import MyApplication

if __name__ == "__main__":
    try:
        MyApplication.run()        
    except ModuleNotFoundError as e:
        print(f"hay un error faltan dependecias por instalar {e}")
    except BaseException as e :
        print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')



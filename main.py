from core.app import MyApplication
import sys
import os
import shutil
import io

# Configurar stdout con encoding UTF-8 para evitar errores de charmap
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def clean_pycache():
    """Elimina cache de Python para evitar problemas con configuraciones antiguas"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, _ in os.walk(base_dir):
        if '__pycache__' in dirs:
            try:
                shutil.rmtree(os.path.join(root, '__pycache__'))
            except:
                pass


if __name__ == "__main__":
    try:
        # Limpiar cache en cada ejecución para evitar problemas
        clean_pycache()

        sys.dont_write_bytecode = True
        MyApplication.start()
    except ModuleNotFoundError as e:
        print(f"hay un error faltan dependecias por instalar {e}")
    except KeyboardInterrupt:
        print('\n\n→ Programa terminado por el usuario')
    except BaseException as e:
        print(
            f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}'
        )


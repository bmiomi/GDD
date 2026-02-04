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


def show_startup_info():
    """Muestra información de inicio de la aplicación"""
    from dotenv import load_dotenv
    
    load_dotenv()
    config_path = os.getenv('CONFIG_PATH')
    
    print("\n" + "="*70)
    print("🚀 GDD - Sistema de Gestión de Distribución")
    print("="*70)
    
    if config_path:
        if os.path.exists(config_path):
            print(f"✓ Configuración Externa: {config_path}")
            print(f"  └─ Plugins leyendo config desde carpeta EXTERNA (editable)")
        else:
            print(f"⚠ CONFIG_PATH definido pero no existe: {config_path}")
            print(f"  └─ Usando config empaquetada como fallback")
    else:
        print(f"ℹ CONFIG_PATH no definido")
        print(f"  └─ Usando config empaquetada (modo desarrollo)")
    
    print("\n💡 Para usar config externa:")
    print("   export CONFIG_PATH=/tu/carpeta/configs  (Linux/macOS)")
    print("   set CONFIG_PATH=C:\\tu\\carpeta\\configs  (Windows CMD)")
    print("   $env:CONFIG_PATH=\"C:\\tu\\carpeta\\configs\" (Windows PowerShell)")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        # Limpiar cache en cada ejecución para evitar problemas
        clean_pycache()

        sys.dont_write_bytecode = True
        
        # Mostrar información de startup
        show_startup_info()
        
        MyApplication.start()
    except ModuleNotFoundError as e:
        print(f"❌ Error: Faltan dependencias por instalar: {e}")
        print(f"💡 Solución: pip install -r requeriment.txt")
    except KeyboardInterrupt:
        print('\n\n→ Programa terminado por el usuario')
    except BaseException as e:
        print(
            f'❌ Error grave que impide la ejecución del programa: {e}'
        )



import csv, os
from utils import print_exception_message, press_enter_key_to_return_to_main_menu, print_success_message

_DEFAULT_ENCODING = "utf-8"
_FILE_NAME = "students_grades.csv"

def _get_file_path():
    return os.path.join(os.path.dirname(__file__),_FILE_NAME)

def _get_if_file_exists():
    if os.path.exists(_get_file_path()):
        return True
    return False

def read_csv_file():
    file_path = _get_file_path()

    if not _get_if_file_exists():
        print_exception_message("El archivo no existe. Proceso cancelado.")
        press_enter_key_to_return_to_main_menu()
        return
    
    try:
        with open(file_path,"r",encoding=_DEFAULT_ENCODING) as file:
            reader = csv.DictReader(file)
            data = list(reader)
            print_success_message("Archivo leído exitosamente.")
            press_enter_key_to_return_to_main_menu()
            return data
    except FileNotFoundError:
        print_exception_message("La ruta del archivo o la ruta no existen.")
    except PermissionError:
        print_exception_message("No tiene permisos para leer el archivo")
    except IsADirectoryError:
        print_exception_message("La ruta corresponde a un directorio, no a un archivo.")
    except OSError as e:
        print_exception_message(f"Error del sistema al leer: {e}")
    except Exception as ex:
        print_exception_message(f"Se presentó un error al crear el archivo: {ex}")

def write_csv_file(data, headers):
    file_path = _get_file_path()

    if _get_if_file_exists():
        print_exception_message("El archivo ya existe. Proceso cancelado.")
        press_enter_key_to_return_to_main_menu()
        return

    try:
        with open(file_path, "w", encoding=_DEFAULT_ENCODING, newline="") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(data)
        print_success_message("Archivo creado exitosamente.")
    except FileNotFoundError:
        print_exception_message("La ruta del archivo o la ruta no existen.")
    except PermissionError:
        print_exception_message("No tiene permisos para escribir el archivo")
    except IsADirectoryError:
        print_exception_message("La ruta corresponde a un directorio, no a un archivo.")
    except OSError as e:
        print_exception_message(f"Error del sistema al escribir: {e}")
    except Exception as ex:
        print_exception_message(f"Se presentó un error al crear el archivo: {ex}")

    press_enter_key_to_return_to_main_menu()
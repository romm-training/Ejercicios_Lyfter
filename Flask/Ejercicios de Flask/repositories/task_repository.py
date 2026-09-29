import json, os

_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")
_DEFAULT_ENCODING = "utf-8"

def _get_if_file_exists(file_path):
    return os.path.exists(file_path)

def read_tasks():
    if not _get_if_file_exists(_FILE_PATH):
        return []
        #raise FileNotFoundError("El archivo de datos no existe en la ruta indicada.")
    
    with open(_FILE_PATH, "r", encoding=_DEFAULT_ENCODING) as file:
        return json.load(file)

def write_tasks(tasks):
    with open(_FILE_PATH, "w", encoding=_DEFAULT_ENCODING) as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)
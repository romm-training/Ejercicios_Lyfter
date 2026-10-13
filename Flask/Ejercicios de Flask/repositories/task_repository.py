import json, os
import logging

logger = logging.getLogger(__name__)

_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")
_DEFAULT_ENCODING = "utf-8"

class RepositoryError(Exception):
    pass

def _get_if_file_exists(file_path):
    return os.path.exists(file_path)

def read_tasks():
    if not _get_if_file_exists(_FILE_PATH):
        return []
    
    try:
        with open(_FILE_PATH, "r", encoding=_DEFAULT_ENCODING) as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
        message = "Error al leer el archivo."
        raise RepositoryError(message) from e


def write_tasks(tasks):
    try:
        with open(_FILE_PATH, "w", encoding=_DEFAULT_ENCODING) as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
    except (FileNotFoundError, Exception) as e:
        message = "Error al escribir el archivo."
        logger.exception(message)
        raise RepositoryError(message) from e
    
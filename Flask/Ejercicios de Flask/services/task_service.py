import logging

from repositories.task_repository import read_tasks, write_tasks, RepositoryError
from utils.http_errors import HTTP_CODES

logger = logging.getLogger(__name__)

_VALID_STATUSES = ["Por Hacer", "En Progreso", "Completada"]

class _FIELD_KEYS():
    TASK_ID = "id"
    TASK_TITLE = "title"
    TASK_DESCRIPTION = "description"
    TASK_STATUS = "status"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'")

def _get_task(tasks, task_id):
    for task in tasks:
        if task[_FIELD_KEYS.TASK_ID] == task_id:
            return task
    return None

# Retorna la lista, el mensaje y el codigo HTTP de respuesta
# Si es existoso, retorna la lista, None y 200
# Si es error, retorna lista vacia, mensaje y 500
def _get_tasks_from_repository() -> tuple[list,str,int]:
    try:
        tasks = read_tasks()
    except RepositoryError:
        return [], "No se pudo leer las tareas", HTTP_CODES.R500

    return tasks, None, HTTP_CODES.R200

# Retorna 200 si existe
# Retorna 404 si no existe
def _get_if_task_exists(tasks, task_id) -> tuple[any,str,int]:
    task = _get_task(tasks, task_id)
    if task is None:
        return None, f"La tarea con id {task_id} no existe", HTTP_CODES.E404
    return task, f"La tarea con id {task_id} ya existe", HTTP_CODES.R200

def _write_tasks_into_repository(tasks) -> tuple[str,int]:
    try:
        write_tasks(tasks)
    except RepositoryError:
        return "No se pudo guardar las tareas", HTTP_CODES.E500

    return "Tareas guardadas exitosamente.", HTTP_CODES.R200 

def get_tasks():
    return _get_tasks_from_repository()

def get_task(task_id):
    tasks, message, code = _get_tasks_from_repository()
    
    return _get_if_task_exists(tasks, task_id)

def _task_id_required(data):
    if not data.get(_FIELD_KEYS.TASK_ID):
        return "El id es requerido."
    return None

def _task_id_is_integer(data):
    if not isinstance(data.get(_FIELD_KEYS.TASK_ID),int):
        return "El id debe ser un numero entero."
    return None

def _task_title_required(data):
    if not data.get(_FIELD_KEYS.TASK_TITLE):
        return "El titulo es requerido."
    else:
        if data[_FIELD_KEYS.TASK_TITLE] == "":
            return "El titulo no puede ser vacío."
    return None

def _task_description_required(data):
    if not data.get(_FIELD_KEYS.TASK_DESCRIPTION):
        return "La descripción es requerida."
    else:
        if data[_FIELD_KEYS.TASK_DESCRIPTION] == "":
            return "La descripción no puede ser vacía."
    return None

def _task_status_required_and_valid(data):
    if not data.get(_FIELD_KEYS.TASK_STATUS):
        return "El estado es requerido"
    if data.get(_FIELD_KEYS.TASK_STATUS) not in _VALID_STATUSES:
        return "Estado invalido"
    return None

def _prepare_validation_messages(messages):
    if len(messages) == 0:
        return None
    return ' '.join(messages)

def validate_task_data_for_creating(data):
    validations = []
    validations.append(_task_id_required(data))
    validations.append(_task_id_is_integer(data))
    validations.append(_task_title_required(data))
    validations.append(_task_description_required(data))
    validations.append(_task_status_required_and_valid(data))
    
    messages = [message for message in validations if message is not None]
    return _prepare_validation_messages(messages)

def validate_task_data_for_updating(data):
    validations = []
    validations.append(_task_title_required(data))
    validations.append(_task_description_required(data))
    validations.append(_task_status_required_and_valid(data))

    messages = [message for message in validations if message is not None]
    return _prepare_validation_messages(messages)

def create_task(data):
    # Validaciones de datos
    error = validate_task_data_for_creating(data)
    if error is not None:
        return None, error, HTTP_CODES.E400

    tasks, message, code = _get_tasks_from_repository()
    if code != HTTP_CODES.R200:
        return tasks, message, code

    # Valida si el id ya existe
    task_id = data[_FIELD_KEYS.TASK_ID]

    task, message, code =_get_if_task_exists(tasks, task_id)
    if code == HTTP_CODES.R200:
        return None, message, HTTP_CODES.E400
    
    # Prepara objeto de la nueva tarea
    new_task = {
        "id": task_id,
        "title": data[_FIELD_KEYS.TASK_TITLE],
        "description": data[_FIELD_KEYS.TASK_DESCRIPTION],
        "status": data[_FIELD_KEYS.TASK_STATUS]
    }

    # Agrega tarea, escribe en archivo y retorna
    tasks.append(new_task)

    message, code = _write_tasks_into_repository(tasks)
    return new_task, message, code

def update_task(task_id, data):
    # Validaciones de datos
    error = validate_task_data_for_updating(data)
    if error is not None:
        return None, error, HTTP_CODES.E400
    
    tasks, message, code = _get_tasks_from_repository()
    if code != HTTP_CODES.R200:
        return tasks, message, code

    task, message, code = _get_if_task_exists(tasks, task_id)
    if code != HTTP_CODES.R200:
        return None, message, code

    task[_FIELD_KEYS.TASK_TITLE] = data[_FIELD_KEYS.TASK_TITLE]
    task[_FIELD_KEYS.TASK_DESCRIPTION] = data[_FIELD_KEYS.TASK_DESCRIPTION]
    task[_FIELD_KEYS.TASK_STATUS] = data[_FIELD_KEYS.TASK_STATUS]

    message, code = _write_tasks_into_repository(tasks)
    return task, message, code


def delete_task(task_id):
    tasks, message, code = _get_tasks_from_repository()
    if code != HTTP_CODES.R200:
        return tasks, message, code
    
    task, message, code = _get_if_task_exists(tasks, task_id)
    if code != HTTP_CODES.R200:
        return task, message, code

    tasks.remove(task)

    message, code = _write_tasks_into_repository(tasks)
    if code != HTTP_CODES.R200:
        return None, message, code

    return None, "Tarea eliminada exitosamente.", HTTP_CODES.R204

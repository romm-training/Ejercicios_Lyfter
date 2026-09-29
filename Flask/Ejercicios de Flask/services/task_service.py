from repositories.task_repository import read_tasks, write_tasks

_VALID_STATUSES = ["Por Hacer", "En Progreso", "Completada"]

def _get_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def get_tasks():
    tasks = read_tasks()
    return tasks, None, 200

def get_task(task_id):
    tasks = read_tasks()
    task = _get_task(tasks, task_id)
    if task is None:
        return None, f"La tarea con el id {task_id} no existe", 404
    return task, None, 200

def validate_task_data(data):
    if not data.get("id"):
        return "El id es requerido"
    if not isinstance(data.get("id"),int):
        return "El id debe ser un numero entero"
    if not data.get("title"):
        return "El titulo es requerido"
    if not data.get("description"):
        return "La descripcion es requerida"
    if not data.get("status"):
        return "El estado es requerido"
    if data.get("status") not in _VALID_STATUSES:
        return "Estado invalido"

    return None

def create_task(data):
    # Validaciones de datos
    error = validate_task_data(data)
    if error is not None:
        return None, error, 400

    # Obtiene las tareas
    tasks = read_tasks()

    # Valida si el id ya existe
    task_id = data["id"]
    task = _get_task(tasks, task_id)
    if task is not None:
        return None, f"La tarea con el id {task_id} ya existe", 400

    # Prepara objeto de la nueva tarea
    new_task = {
        "id": task_id,
        "title": data["title"],
        "description": data["description"],
        "status": data["status"]
    }

    # Agrega tarea, escribe en archivo y retorna
    tasks.append(new_task)
    write_tasks(tasks)
    return new_task, None, 201

def update_task(task_id, data):
    tasks = read_tasks()
    task = _get_task(tasks, task_id)
    if task is None:
        return None, f"La tarea con id {task_id} no existe", 404

    if "title" in data:
        if not data["title"]:
            return None, "El titulo no puede estar vacío", 400
        task["title"] = data["title"]

    if "description" in data:
        if not data["description"]:
            return None, "La descripcion no puede estar vacia", 400
        task["description"] = data["description"]

    if "status" in data:
        if data["status"] not in _VALID_STATUSES:
            return None, f"Estado invalido. Valores permitidos: {', '.join(_VALID_STATUSES)}", 400
        task["status"] = data["status"]

    write_tasks(tasks)
    return task, None, 200

def delete_task(task_id):
    tasks = read_tasks()
    task = _get_task(tasks, task_id)
    if task is None:
        return None, f"La tarea con id {task_id} no existe", 404

    tasks.remove(task)
    write_tasks(tasks)
    return None, None, 204

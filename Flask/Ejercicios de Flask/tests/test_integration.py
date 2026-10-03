import pytest, json
from app import app

_BASE_URI = "/api/v1/tasks"

@pytest.fixture(scope="session")
def tasks_file(tmp_path_factory):
    file = tmp_path_factory.mktemp("data") / "tasks.json"
    file.write_text("[]", encoding="utf-8")
    return file

@pytest.fixture
def client(monkeypatch, tasks_file):
    monkeypatch.setattr(
        "repositories.task_repository._FILE_PATH", str(tasks_file)
    )
    app.config["TESTING"] = True
    return app.test_client()

new_task_1 = {
    "description": "Prueba ejercicio de Flask 1",
    "id": 1,
    "status": "Por Hacer",
    "title": "Ejercicio de Flask 1"
}

new_task_2 = {
    "description": "Prueba ejercicio de Flask 2",
    "id": 2,
    "status": "Completada",
    "title": "Ejercicio de Flask 2"
}

new_task_3 = {
    "description": "Prueba ejercicio de Flask 3",
    "id": 3,
    "status": "En Progreso",
    "title": "Ejercicio de Flask 3"
}

def test_create_tasks_successful(client, tasks_file):
    response = client.post(_BASE_URI, json=new_task_1)
    assert response.status_code == 201, response.get_json()

    response = client.get(f"{_BASE_URI}/1")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(new_task_1, sort_keys=True)

    response = client.post(_BASE_URI, json=new_task_2)
    assert response.status_code == 201, response.get_json()
    
    response = client.get(f"{_BASE_URI}/2")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(new_task_2, sort_keys=True)

    response = client.post(_BASE_URI, json=new_task_3)
    assert response.status_code == 201, response.get_json()

    response = client.get(f"{_BASE_URI}/3")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(new_task_3, sort_keys=True)

def test_create_task_existing_id(client, tasks_file):
    expected_response_1 = {
        "error": "La tarea con id 1 ya existe."
    }

    expected_response_2 = {
        "error": "La tarea con id 2 ya existe."
    }
    
    response = client.post(_BASE_URI, json=new_task_1)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json()) == json.dumps(expected_response_1)

    response = client.post(_BASE_URI, json=new_task_2)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json()) == json.dumps(expected_response_2)

def test_create_task_no_id(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "status": "Completada",
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "El id es requerido. El id debe ser un número entero."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json()) == json.dumps(expected_response)

def test_create_task_empty_id(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "id": "",
        "status": "Completada",
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "El id es requerido. El id debe ser un número entero."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json()) == json.dumps(expected_response)

def test_create_task_invalid_id(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "id": "A",
        "status": "Completada",
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "El id debe ser un número entero."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json()) == json.dumps(expected_response)

def test_create_task_no_description(client, tasks_file):
    new_invalid_task = {
        "id": 2,
        "status": "Completada",
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "La descripción es requerida."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_create_task_empty_description(client, tasks_file):
    new_invalid_task = {
        "description": "",
        "id": 2,
        "status": "Completada",
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "La descripción es requerida."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_create_task_no_title(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "id": 2,
        "status": "Completada"
    }

    expected_response = {
        "error": "El título es requerido."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_create_task_empty_title(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "id": 2,
        "status": "Completada",
        "title": ""
    }

    expected_response = {
        "error": "El título es requerido."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

response_invalid_status = {
    "error": "Estado inválido."
}

def test_create_task_invalid_status(client, tasks_file):
    new_task_invalid_status = {
        "description": "Prueba ejercicio de Flask 2",
        "id": 2,
        "status": "Completado",
        "title": "Ejercicio de Flask 2"
    }
    
    response = client.post(_BASE_URI, json=new_task_invalid_status)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(response_invalid_status, sort_keys=True)

def test_create_task_no_status(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "id": 2,
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "El estado es requerido."
    }

    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_create_task_empty_status(client, tasks_file):
    new_invalid_task = {
        "description": "Prueba ejercicio de Flask 2",
        "id": 2,
        "status": "",
        "title": "Ejercicio de Flask 2"
    }

    expected_response = {
        "error": "El estado es requerido."
    }
    
    response = client.post(_BASE_URI, json=new_invalid_task)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_get_tasks_successful(client):
    response = client.get(_BASE_URI)
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps([new_task_1,new_task_2,new_task_3], sort_keys=True)

def test_get_tasks_status_por_hacer(client):
    response = client.get(f"{_BASE_URI}?status=Por Hacer")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps([new_task_1], sort_keys=True)

def test_get_tasks_status_completada(client):
    response = client.get(f"{_BASE_URI}?status=Completada")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps([new_task_2], sort_keys=True)

def test_get_tasks_status_en_progreso(client):
    response = client.get(f"{_BASE_URI}?status=En Progreso")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps([new_task_3], sort_keys=True)

def test_get_tasks_status_invalid_status(client):
    response = client.get(f"{_BASE_URI}?status=Prueba")
    assert response.status_code == 400
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(response_invalid_status, sort_keys=True)

def test_get_tasks_status_empty_status(client):
    response = client.get(f"{_BASE_URI}?status=")
    assert response.status_code == 400
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(response_invalid_status, sort_keys=True)

def test_get_task_successful(client):
    response = client.get(f"{_BASE_URI}/1")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(new_task_1, sort_keys=True)

def test_get_task_no_existing_id(client):
    response = client.get(f"{_BASE_URI}/99")

    expected_response = {
        "error": "La tarea con id 99 no existe."
    }
    
    assert response.status_code == 404
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_get_task_invalid_id(client):
    response = client.get(f"{_BASE_URI}/A")

    expected_response = {
        "error": "El id debe ser numérico."
    }
    
    assert response.status_code == 404
    assert json.dumps(response.get_json(), sort_keys=True) == 'null'

def test_get_task_empty_id(client):
    response = client.get(f"{_BASE_URI}/")

    expected_response = {
        "error": "El id debe ser numérico."
    }
    
    assert response.status_code == 404
    assert json.dumps(response.get_json(), sort_keys=True) == 'null'

def test_update_task_successful(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = {
        "description": "Prueba ejercicio de Flask 11",
        "id": 1,
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    response = client.put(f"{_BASE_URI}/1", json=task_to_update)
    assert response.status_code == 200, response.get_json()

    response = client.get(f"{_BASE_URI}/1")
    assert response.status_code == 200
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_no_existing_id(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = {
        "error": "La tarea con id 99 no existe."
    }

    response = client.put(f"{_BASE_URI}/99", json=task_to_update)
    assert response.status_code == 404, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_invalid_id(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = "null"

    response = client.put(f"{_BASE_URI}/A", json=task_to_update)
    assert response.status_code == 404, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == expected_response

def test_update_task_no_description(client, tasks_file):
    task_to_update = {
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = {
        "error": "La descripción es requerida."
    }

    response = client.put(f"{_BASE_URI}/1", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_empty_description(client, tasks_file):
    task_to_update = {
        "description": "",
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = {
        "error": "La descripción es requerida."
    }

    response = client.put(f"{_BASE_URI}/1", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_no_title(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "Por Hacer"
    }

    expected_response = {
        "error": "El título es requerido."
    }

    response = client.put(f"{_BASE_URI}/1", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_empty_title(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "Por Hacer",
        "title": ""
    }

    expected_response = {
        "error": "El título es requerido."
    }

    response = client.put(f"{_BASE_URI}/99", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_no_status(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = {
        "error": "El estado es requerido."
    }

    response = client.put(f"{_BASE_URI}/1", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_empty_status(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "",
        "title": "Ejercicio de Flask 11"
    }

    expected_response = {
        "error": "El estado es requerido."
    }

    response = client.put(f"{_BASE_URI}/99", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_update_task_empty_status(client, tasks_file):
    task_to_update = {
        "description": "Prueba ejercicio de Flask 11",
        "status": "Prueba",
        "title": "Ejercicio de Flask 11"
    }

    response = client.put(f"{_BASE_URI}/99", json=task_to_update)
    assert response.status_code == 400, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(response_invalid_status, sort_keys=True)

def test_delete_task_successful(client, tasks_file):
    expected_response = {
        "description": "Prueba ejercicio de Flask 11",
        "id": 1,
        "status": "Por Hacer",
        "title": "Ejercicio de Flask 11"
    }

    response = client.delete(f"{_BASE_URI}/1")
    assert response.status_code == 204, response.get_json()

    response = client.get(f"{_BASE_URI}/1")
    assert response.status_code == 404

def test_update_task_no_existing_id(client, tasks_file):
    expected_response = {
        "error": "La tarea con id 99 no existe."
    }

    response = client.delete(f"{_BASE_URI}/99")
    assert response.status_code == 404, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == json.dumps(expected_response, sort_keys=True)

def test_delete_task_invalid_id(client, tasks_file):
    expected_response = "null"

    response = client.delete(f"{_BASE_URI}/A")
    assert response.status_code == 404, response.get_json()
    assert json.dumps(response.get_json(), sort_keys=True) == expected_response

import pytest
from unittest.mock import patch

from app import app

tasks = [
  {
    "id": 1,
    "title": "Ejercicio de Flask 1",
    "description": "Prueba ejercicio de Flask 1",
    "status": "Por Hacer"
  },
  {
    "id": 2,
    "title": "Ejercicio de Flask 2",
    "description": "Prueba ejercicio de Flask 2",
    "status": "Por Hacer"
  },
  {
    "id": 3,
    "title": "Ejercicio de Flask 3",
    "description": "Prueba ejercicio de Flask 3",
    "status": "Por Hacer"
  }
]

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

# GET /api/v1/tasks
def test_get_tasks_exitoso(client):
    with patch("services.task_service.get_tasks", return_value=(tasks, None, 200)):
        response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert response.get_json() == tasks

# Get /api/v1/tasks/<id>
def test_get_task_existente(client):
    task = {
        "id": 1,
        "title": "Ejercicio de Flask 1",
        "description": "Prueba ejercicio de Flask 1",
        "status": "Por Hacer"
    }

    with patch("services.task_service.get_task", return_value=(task, None, 200)):
        response = client.get("/api/v1/tasks/1")

        assert response.status_code == 200
        assert response.get_json() == task

def test_get_task_no_existente(client):
    with patch("services.task_service.get_task", return_value=(None, "Tarea no encontrada", 404)):
        response = client.get("/api/v1/tasks/99")

        assert response.status_code == 404
        assert response.get_json() == {"error": "Tarea no encontrada"}

# POST /api/v1/tasks
def test_create_task_exitoso(client):
    payload = {
        "id": 1,
        "title": "Ejercicio de Flask 1",
        "description": "Prueba ejercicio de Flask 1",
        "status": "Por Hacer"
    }

    with patch("services.task_service.create_task", return_value=(payload, None, 201)) as mock_create:
        response = client.post("/api/v1/tasks", json=payload)

    assert response.status_code == 201
    assert response.get_json() == payload
    mock_create.assert_called_once_with(payload)

def test_create_task_error_validacion(client):
    with patch("services.task_service.create_task", 
               return_value=(None, "Estado invalido", 400)):
        response = client.post("/api/v1/tasks", json={"title":"A"}) 

    assert response.status_code == 400
    assert response.get_json() == {"error": "Estado invalido"}


    
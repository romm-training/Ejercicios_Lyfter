import pytest
from app import app

_BASE_URI = "/api/v1/tasks"

@pytest.fixture
def client(tmp_path, monkeypatch):
    temp_tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr(
        "repositories.task_repository._FILE_PATH", str(temp_tasks_file)
    )
    app.config["TESTING"] = True
    return app.test_client()

def test_get_tasks_exitoso(client):
    response = client.get(_BASE_URI)
    assert response.status_code == 200

def test_create_task_exitoso(client):
    new_task = {
        "id": 1,
        "title": "Ejercicio de Flask 1",
        "description": "Prueba ejercicio de Flask 1",
        "status": "Por Hacer"
    }

    assert client.post(_BASE_URI, json=new_task).status_code == 201

    response = client.get(f"{_BASE_URI}/1")
    assert response.status_code == 200
    assert response.get_json() == new_task
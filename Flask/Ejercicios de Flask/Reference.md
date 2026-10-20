# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A student exercise (Lyfter "Flask" module): a small JSON REST API for managing tasks (CRUD), persisted to a local JSON file. User-facing messages and task statuses are in Spanish. The sibling folder `../Teoria/hello_world_api.py` holds the module's theory example.

## Instructions

Do not apply changes to project files without explicit approval from the user — explain and propose (with example snippets) by default.

Do no create code. You only have to answer questions.

## Commands

Run from this directory (`Ejercicios de Flask`) using the venv's Python (Flask 3.1 is installed in `.venv`; there is no requirements.txt):

```
.venv\Scripts\python.exe app.py
```

This starts the dev server with `debug=True` on `http://127.0.0.1:5000`. Endpoints live under `/api/v1/tasks` (`GET`, `POST`) and `/api/v1/tasks/<int:task_id>` (`GET`, `PUT`, `DELETE`).

`tests/` exists but is empty; no test framework is installed in `.venv` yet.

## Architecture

Three layers, each only calling the one below it. Imports are absolute from the project root (`from services import ...`), so the app must be run from this directory.

- **`app.py`** — creates the `Flask` app and calls `register_task_routes(app)`.
- **`routes/tasks_routes.py`** — `register_task_routes(app)` defines the view functions as closures (no Blueprint). Each handler parses `request.get_json(silent=True) or {}`, calls the service, and turns its result into a JSON response.
- **`services/task_service.py`** — business logic and validation. **Every service function returns a `(result, error, status_code)` tuple**; routes check `error` and return `{"error": error}` with that code, otherwise `jsonify(result)`. Keep new service functions in this shape. Valid statuses are in `_VALID_STATUSES` (`"Por Hacer"`, `"En Progreso"`, `"Completada"`). Task shape: `{id, title, description, status}`.
- **`repositories/task_repository.py`** — `read_tasks()` / `write_tasks(tasks)` over `data/tasks.json`, resolved relative to the module file (not the CWD). Every write rewrites the whole list read earlier.

## Known issues in the current code

The exercise is in progress; these are existing bugs to be aware of (not to fix silently):

- `write_tasks` opens the file in append mode (`"a"`), which corrupts the JSON on the second write, and returns early without writing if `data/tasks.json` doesn't exist — and `data/` is currently empty, so nothing is ever persisted.
- `_get_task` compares `task["id"] == task.id` (should use the `task_id` argument; `task.id` raises `AttributeError` on a dict).
- `delete_task` calls `_get_task(task_id)` without the `tasks` argument.
- The `GET /<task_id>` route calls `task_service.get_tasks()` instead of `get_task(task_id)`.
- `create_task` does no validation (missing keys raise `KeyError` → 500), doesn't check status against `_VALID_STATUSES`, and takes `id` from the client without checking for duplicates.

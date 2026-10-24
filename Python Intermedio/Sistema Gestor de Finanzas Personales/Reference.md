# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A desktop personal-finance manager built with FreeSimpleGUI (a PySimpleGUI fork). This is a student exercise (Lyfter "Python Intermedio" module) whose goal is to practice: modularization, file handling, validations, functions, OOP, and separation of logic/presentation. Full requirements are in `Instrucciones.md` — read it before implementing features, since it defines exact expected input/output formats.

Core requirements (`Instrucciones.md`): movements table on the main window, add-category/add-gasto/add-ingreso sub-windows, an error message when adding a movement with no categories available for that type, and CSV-backed persistence loaded on startup. Optional/extra requirements, not yet implemented: date-range filtering (main window has `FROM_DATE`/`TO_DATE` fields and a "Filtrar" button, but the handler currently only does `print("Filtrar")`), custom/validated movement dates (currently `values[MOVEMENT_DATE]` is stored raw with no format/future-date validation), CSV export with income/expense/balance totals, and per-category colors applied to table rows.

## Instructions

Always start manual mode on. Neve do changes without manual approval.

## Commands

Run from this directory (`Sistema Gestor de Finanzas Personales`), using the venv's Python:

```
.venv\Scripts\python.exe interfaz.py
```

Dependencies are installed in `.venv` (FreeSimpleGUI). There is no requirements.txt yet — check `.venv\Lib\site-packages` if you need to know what's installed, or reinstall with `.venv\Scripts\pip.exe install freesimplegui`.

No test suite exists yet. The instructions require a separate `test_logica.py` (or similar) with **at least 8 unit tests** covering business logic/validations, runnable independently of the GUI (i.e., test the `business/` layer, not `interfaz.py`). Once created, run tests with `.venv\Scripts\python.exe -m pytest` or `.venv\Scripts\python.exe -m unittest`.

## Architecture

Layered structure, each layer only talking to the one directly below it:

- **`interfaz.py`** — the single GUI entry point/module (FreeSimpleGUI). Defines `_CONSTANTS`/`_KEYS` helper classes (both raise `AttributeError` on any attempted attribute mutation, so they behave as read-only constant holders), the main window (movements table + filter/action buttons), and two sub-window functions: `movement_screen(movement_type)` for adding an Ingreso/Gasto, and `category_screen()` for adding a Categoria. Calls into `business/` only, never `persistency/` directly. The main event loop hides the main window (`window.hide()`) while a sub-window is open and calls `window.UnHide()` + reloads table data afterward.
- **`business/`** — thin logic layer (`movement_biz.py`, `category_biz.py`). `Movement_Biz` exposes `add_data`/`read_data`; `Category_Biz` exposes `append_data`/`read_data` (naming differs between the two — check the actual method name before calling). Both wrap the matching `persistency/` module and swallow `FileNotFoundError` into an empty list on read.
- **`dto/`** — plain data classes (`movement_dto.py`: `Movement_Dto(date, type, category, description, amount)`, `category_dto.py`: `Category_Dto(movement_type, name, color)`) with `to_dict()` and a classmethod `headers()` used to derive CSV column order/names from the DTO field order. `headers()` order must match `__init__` positional order and CSV column order in persistency read/write functions.
- **`persistency/`** — CSV I/O (`persistency_movement.py` → `persistency/movements.csv`, `persistency_category.py` → `persistency/categories.csv`), using `csv.DictReader`/`csv.DictWriter` keyed off each module's own `_HEADERS` (derived from the matching DTO's `headers()`). Files are located relative to the persistency module's own path via `os.path.dirname(__file__)`, not the CWD. `append_data` creates the file with a header row on first write (checked via `_get_if_file_exists`), then appends rows on subsequent calls.

Data flow for reads: `persistency.read_data()` (raises `FileNotFoundError` if the CSV doesn't exist) → `business.read_data()` (catches that, returns `[]`) → `interfaz.py` (renders into an `sg.Table` via `load_table_data()`).

Data flow for writes: DTO built from GUI form `values` dict (from `window.read()`) → `business.add_data`/`append_data` → `persistency.append_data`.

## Things to watch for while editing

- `Category_Biz` uses `append_data` while `Movement_Biz` uses `add_data` for the equivalent write operation — don't assume the two business classes are symmetric.
- Movement dates and category colors are stored as free-form strings straight from GUI input, with no validation performed anywhere in the stack yet — anything implementing the optional date-validation or color-coding requirements needs to add that validation itself (likely in `business/`, per the logic/presentation separation).

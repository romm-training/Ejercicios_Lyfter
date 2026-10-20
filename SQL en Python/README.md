# Alquiler de autos: Flask + PostgreSQL (psycopg2)

API REST para gestionar autos, usuarios y alquileres (esquema `lyfter_car_rental`). El foco técnico del ejercicio es el **cambio de estados**: las reglas se declaran en un YAML y un motor genérico las ejecuta de forma transaccional.

Código en `Ejercicios_de_SQL_en_Python/`. La carpeta `Teoria/` son ejercicios de apoyo y no forma parte de la solución.

## Arquitectura en capas

```
routes/  →  services/  →  repositories/  →  infrastructure/db.py
(HTTP)      (negocio)      (SQL)              (conexión)
```

| Capa | Responsabilidad |
|---|---|
| `routes/` | Recibe HTTP, llama al servicio y traduce excepciones a códigos HTTP (404, 409, 422, 500). Una función `register_*_routes(app, service)` por entidad. |
| `services/` | Un servicio por entidad (`car`, `user`, `car_rental`), capa fina que delega el cambio de estado al motor (`state_machine.py`). |
| `services/rules/` | Guards y efectos de las transiciones (`car_rules.py`, `user_rules.py`, `car_rental_rules.py`). |
| `repositories/` | CRUD por entidad. Solo SQL parametrizado; devuelve diccionarios (`_format_record`). No conoce las reglas de estado ni controla `commit`/`rollback`. |
| `infrastructure/db.py` | `PgManager`: único archivo que maneja la conexión. |
| `exceptions.py` | `NotFoundError`, `BusinessRuleError`, `InvalidTransitionError`. |
| `config/state_transitions.yaml` | Reglas de transición (datos, no código). |

`app.py` es la raíz de composición: carga `.env`, crea `PgManager.from_env()`, construye el motor y **inyecta** las dependencias en repositorios, servicios y rutas.

## Patrones y buenas prácticas

- **Máquina de estados declarativa.** Estados, transiciones, guards y efectos se definen en el YAML. Una transición que no está en el YAML queda prohibida (no se listan las inválidas). Recombinar reglas existentes solo requiere editar el YAML.
- **Guards y efectos con registro por decoradores.** `@guard("nombre")` y `@effect("nombre")` guardan la función en un registro y lanzan error si el nombre ya existe. El registro ocurre al importar los módulos de `services/rules/`, por eso `build_state_machine` los importa antes de cargar el YAML.
- **Validación fail-fast al arrancar** (`load_transitions`): entidad desconocida, estados duplicados, estado no declarado, guard/efecto no registrado, transición duplicada o más de un estado inicial por entidad detienen la app antes de atender peticiones.
- **Carga segura de YAML** con `yaml.safe_load()`.
- **Creación como transición.** Crear un registro es la transición `from: null → estado inicial`, así pasa por los mismos guards y efectos que cualquier cambio.
- **Transacciones atómicas.** `PgManager.transaction()` es un context manager con contador de profundidad (`_depth`): `execute_query` solo hace `commit` cuando `_depth == 0`, y solo el bloque más externo confirma o revierte. Validaciones, `UPDATE` y efectos sobre otras tablas se aplican juntos o no se aplica nada.
- **Concurrencia.** `SELECT ... FOR UPDATE` en los repositorios (`get_by_id_for_update`) dentro de la transacción, y un `threading.RLock` que serializa el acceso a la única conexión compartida (Flask atiende en varios hilos).
- **Inyección de dependencias** por constructor (repositorios → servicios → rutas, motor → servicios); facilita probar con mocks.
- **Contexto explícito** (`Context` dataclass) que se pasa a guards y efectos: entidad, estado destino, repositorios, registro actual y datos de entrada.
- **`StrEnum` por entidad** (`services/enums/statuses.py`) como fuente única de nombres de estado en Python.
- **Configuración por entorno.** `python-dotenv` + variables de entorno; las obligatorias se leen con `os.environ[...]` para fallar al arrancar si faltan. `.env` no se versiona; `.env.example` documenta las variables.
- **SQL seguro.** Consultas parametrizadas (`%s`); los filtros de `get_all` se validan contra una lista blanca de columnas.
- **Estado protegido.** El `PUT` genérico no cambia el estado directamente: el servicio separa el campo de estado y lo envía al motor; los campos inmutables del alquiler (`car_id`, `user_id`, `rental_date_at`) se rechazan en la ruta.
- **Errores de dominio** (`NotFoundError`, `BusinessRuleError`, `InvalidTransitionError`) separados de los técnicos y mapeados a HTTP en `routes/`.
- **Pruebas unitarias** con `pytest` y `MagicMock` (sin BD ni servidor): repositorio, reglas, servicio y rutas de `user` (en `tests/`).

## Flujo del motor

`change_status(entity, id, target)`:

1. Abre `with db.transaction()` y lee el registro con `FOR UPDATE`.
2. Busca `(entidad, estado_actual, destino)` en la tabla de transiciones; si no existe → `InvalidTransitionError`.
3. Ejecuta los **guards** en orden (cualquiera puede lanzar `BusinessRuleError`).
4. Actualiza el estado (`update_status`).
5. Ejecuta los **efectos** sobre otras tablas, en la misma transacción.
6. `commit`; cualquier excepción produce `rollback`.

`create(entity, data)` sigue el mismo flujo con `from: null`, ejecutando guards, `INSERT` y efectos.

## Estados y transiciones por entidad

Los estados son `varchar(20)` sin `CHECK`/`ENUM`; la validación vive en el motor. Lo siguiente refleja `config/state_transitions.yaml`.

### `car_rental` (dirige a las otras entidades)

| Transición | Guards | Efectos |
|---|---|---|
| (crear) → `pending` | auto disponible, usuario activo | auto → `reserved` |
| `pending` → `active` | auto reservado, usuario activo | auto → `rented` |
| `pending` → `cancelled` | alquiler pendiente, usuario activo | auto → `available` |
| `active` → `completed` | alquiler activo, auto `rented`, usuario activo | auto → `available` |
| `active` → `overdue` | alquiler activo, usuario activo | usuario → `delinquent` |
| `overdue` → `completed` | alquiler vencido, usuario moroso | usuario → `active`, auto → `available` |

`completed` y `cancelled` son estados finales.

### `car`

`available` → `maintenance` | `inactive` | `sold`; `maintenance` → `available` | `inactive` | `sold`; `inactive` → `sold`. Alta en `available`.
Los estados `reserved` y `rented` **no** se alcanzan manualmente: solo los fija un alquiler mediante sus efectos (`car_to_reserved`, `car_to_rented`).

### `user`

Alta en `active`. `active` ⇄ `inactive`; `active` → `delinquent`; `delinquent` → `active`. Pasar a `inactive` exige no tener alquileres abiertos (`pending`, `active`, `overdue`). El alta valida que `username` y `email` no existan.

## Ejecución

1. Ejecutar en orden los scripts de `postgres/` (01 a 06; 03 a 05 incluyen datos de ejemplo).
2. Copiar `.env.example` a `.env` y completar `DB_NAME`, `DB_USER`, `DB_PASSWORD` (y `STATUS_TRANSITIONS_PATH`, ej. `config/state_transitions.yaml`).
3. Dependencias en el `.venv`: `flask`, `psycopg2-binary`, `pyyaml`, `python-dotenv`, `pytest`.
4. Iniciar: `python app.py` (desde `Ejercicios_de_SQL_en_Python/`). Tests: `pytest`.

Endpoints: `/api/v1/users`, `/api/v1/cars`, `/api/v1/rentals` (GET lista con filtros, GET por id, POST, PUT, DELETE).

## Limitaciones conocidas

- Una sola conexión compartida y serializada con `RLock`; el pool de conexiones (`DB_POOL_MIN/MAX`) está pendiente y hoy esas variables no se usan.
- La traducción de errores a HTTP se repite en cada ruta; queda pendiente centralizarla con `@app.errorhandler` (y una base común `AppError`).
- Pendientes de las reglas de negocio: validar `return_date_at > rental_date_at`, exigir `now() > return_date_at` para `overdue`, impedir dos alquileres abiertos por auto, y cambiar de estado un auto sin alquileres abiertos.
- Pendientes en BD: `CHECK` de estados, índice único parcial `uq_car_open_rental`, tabla `status_history`.
- Pruebas unitarias hechas solo para `user`; faltan `car`, `car_rental` y la tabla de transiciones.
- El esquema no registra fecha real de devolución ni pagos, por lo que la morosidad no se puede verificar en BD.

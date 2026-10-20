# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto

Ejercicios del curso sobre usar Postgres con Python. El objetivo es que me ayudes con temas que te consulte. Solo propuestas y explicaciones; no editar ni crear archivos salvo que lo pida explícitamente.

## Instrucciones

Se puntual y directo en resolver lo que se solicita. 
No des muchas expliciones a menos que se solicite. 
Respuestas de dos lineas maximo.
Si se te pide que hagas algo en un archivo, solo hazlo. No expliques lo que hiciste.

## Entorno

- Entorno virtual en `.venv/` (Python 3.13; paquete actual: `psycopg2-binary`; planificados: `pyyaml`, `python-dotenv`). En PowerShell: `.venv\Scripts\Activate.ps1`.
- Requiere PostgreSQL en `localhost:5432` (usuario `postgres`, base `postgres`).
- Configuración por variables de entorno, cargadas desde un archivo `.env` con `python-dotenv` (nueva dependencia del `.venv`, junto con `pyyaml`). `.env` va en `.gitignore`; se versiona un `.env.example` con los nombres de las variables y sin valores reales. Variables: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` (por defecto `localhost`), `DB_PORT` (por defecto `5432`) y, opcional, `STATUS_TRANSITIONS_PATH`. `DB_POOL_MIN` y `DB_POOL_MAX` se usarán solo cuando se añada el pool (mejora posterior). Las obligatorias se leen con `os.environ[...]` para fallar al arrancar si faltan.
- Ejecutar un script de teoría: `.venv\Scripts\python.exe Teoria\first_db_connection.py`

## Estructura

- Omitir por completo carpeta `Teoria/`.
- `Ejercicios_de_SQL_en_Python/`: proyecto de alquiler de autos (esquema `lyfter_car_rental`), en capas:
  - `Postgres/`: scripts SQL numerados (01 base de datos, 02 esquema, 03 `car`, 04 `user`, 05 `car_rental`, 06 pruebas básicas). Ejecutar en orden; 03 a 05 incluyen datos de ejemplo.
  - `infrastructure/db.py`: `PgManager` (una conexión psycopg2, `execute_query`, `close_connection`; planificado: `transaction()` y `from_env()`; el pool de conexiones es una mejora posterior; ver "Piezas de apoyo"). Unico archivo que maneja la conexion con BD.
  - `repositories/`: CRUD por entidad (`car`, `user`, `car_rental`) que recibe un `db_manager` y devuelve diccionarios vía `_format_record`.
  - `app.py`: punto de entrada Flask (`app.run(debug=True)`). Por ahora solo configura logging y crea la app; el registro de rutas está comentado y no instancia `PgManager`. Planificado: cargar el `.env`, crear `PgManager.from_env()`, construir el motor (`build_state_machine`) y los servicios con sus dependencias inyectadas, y cerrar la conexión al apagar.
  - `errors.py` (planificado, en la raíz junto a `app.py`): todas las excepciones propias en un solo archivo, con una base común `AppError(Exception)` de la que heredan `NotFoundError`, `InvalidTransitionError`, `BusinessRuleError` y `DatabaseUnavailableError` (esta última solo con el pool). Lo importan repositorios, servicios, motor y `routes/`.
  - `services/` y `routes/`: archivos creados pero vacíos (pendientes de implementar). Estructura planificada (ver "Diseño técnico propuesto"):
    - `config/status_transitions.yaml`: reglas de transición (datos). Carpeta nueva dentro de `Ejercicios_de_SQL_en_Python/`.
    - `services/state_machine.py`: motor genérico, registro de guards/efectos (decoradores) y carga/validación del YAML.
    - `services/<entidad>_service.py`: capa fina sobre el motor, una por entidad (`car`, `user`, `car_rental`).
    - `services/<entidad>_rules.py`: guards y efectos de las transiciones de esa entidad.
- Dependencias entre capas: `routes/` → `services/` → `repositories/` → `infrastructure/db.py`. Nadie salta capas, con una excepción: `services/` abre las transacciones con `db.transaction()` (ver "Piezas de apoyo").
- Relaciones: `car_rental.car_id` → `car.id` y `car_rental.user_id` → `user.id`.

## Estados

Las columnas son `varchar(20) NOT NULL` sin `CHECK` ni `ENUM`; ni la BD ni los repositorios validan los valores. Los estados válidos son los siguientes (valores en inglés):

- `user.account_status`: `active`, `inactive`, `delinquent` (moroso).
- `car.status`: `available`, `reserved`, `rented`, `maintenance`, `inactive`, `sold`.
- `car_rental.status`: `pending`, `active`, `completed`, `cancelled`, `overdue`.

Flujo secuencial esperado (aún no implementado en `services/`):

- `car_rental`: `pending` → `active` → `completed`; `active` → `overdue` → `completed`; `pending` → `cancelled`.
- `car`: `available` → `reserved` → `rented` → `available`; `available` → `maintenance` → `available`; `available` o `maintenance` → `inactive` o `sold` (finales).
- `user`: `active` ⇄ `inactive`; `active` ⇄ `delinquent` (el cambio a moroso lo envía directamente el frontend, por pagos o devoluciones vencidas).

## Reglas de negocio para cambios de estado

### Reglas generales

1. El registro debe existir (`id` válido).
2. El estado nuevo debe estar en el catálogo de su entidad (la BD no lo valida; hacerlo en el servicio).
3. El estado nuevo debe ser distinto del actual.
4. La transición debe estar en las transiciones permitidas de la entidad.
5. Validaciones y `UPDATE` en una sola transacción, leyendo los registros con `SELECT ... FOR UPDATE`.
6. Si el cambio afecta a otra tabla, los efectos se aplican juntos o no se aplica nada.
7. Una vez creado un `car_rental`, los campos `user_id`, `car_id` y `rental_date_at` no pueden actualizarse. Solo se pueden cambiar `return_date_at` y `status` (este último solo por `update_status`).

### `car_rental` (dirige a las otras entidades)

| Transición | Condiciones | Efecto |
|---|---|---|
| (crear) → `pending` | Usuario `active`. Auto `available`. `return_date_at` > `rental_date_at`. Auto sin otro alquiler abierto. | Auto → `reserved` |
| `pending` → `active` | Usuario sigue `active`. Auto `reserved` y asociado a este alquiler. | Auto → `rented` |
| `pending` → `cancelled` | Sin condiciones adicionales. | Auto → `available` |
| `active` → `completed` | Auto en `rented`. | Auto → `available` |
| `active` → `overdue` | `now() > return_date_at`. | Ninguno (la morosidad del usuario la define el frontend) |
| `overdue` → `completed` | Auto en `rented`. | Auto → `available` |

Inválidas: salir de `completed` o `cancelled` (finales); `active` → `pending` o `cancelled`; `overdue` → `cancelled` o `active`; `pending` → `completed` u `overdue`.

### `car`

| Transición | Condiciones |
|---|---|
| `available` → `reserved` | Solo mediante un alquiler `pending` nuevo. Sin otro alquiler abierto. |
| `reserved` → `rented` | Existe un alquiler `pending` que pasa a `active`. |
| `reserved` → `available` | El alquiler `pending` está `cancelled`. |
| `rented` → `available` | El alquiler `active` u `overdue` pasa a `completed`. |
| `available` → `maintenance` | Sin alquileres abiertos (`pending`, `active`, `overdue`). |
| `maintenance` → `available` | Sin alquileres abiertos. |
| `available` o `maintenance` → `inactive` o `sold` | Sin alquileres abiertos. Estados finales. |

Inválidas: salir de `inactive` o `sold`; cambios manuales desde `rented` o `reserved` que no pasen por el alquiler; `reserved` → `maintenance`, `inactive` o `sold`; `rented` → `sold` o `inactive`.

### `user`

| Transición | Condiciones |
|---|---|
| `active` → `inactive` | Sin alquileres abiertos (`pending`, `active`, `overdue`). |
| `inactive` → `active` | Sin condiciones de BD (opcional: validar datos del perfil). |
| `active` → `delinquent` | Solicitado directamente desde el frontend. No exige un alquiler `overdue`. |
| `delinquent` → `active` | Solicitado directamente desde el frontend (deuda saldada). |
| `delinquent` → `inactive` | Sin alquileres abiertos. |
| `inactive` → `delinquent` | Inválida: solo un usuario `active` puede pasar a moroso. |

Un usuario que no esté `active` no puede crear ni activar alquileres.

### Invariantes entre tablas

Comprobar antes y después de cada cambio:

1. Un auto tiene como máximo un alquiler abierto (`pending`, `active` u `overdue`).
2. Auto `reserved` ⇔ existe un alquiler `pending` para él.
3. Auto `rented` ⇔ existe un alquiler `active` u `overdue` para él.
4. Auto `available`, `maintenance`, `inactive` o `sold` ⇒ sin alquileres abiertos.
5. Usuario `inactive` ⇒ sin alquileres abiertos.

### Orden recomendado en los scripts

El estado del alquiler dirige; auto y usuario se actualizan como consecuencia. Cambiar un auto o un usuario por separado solo se permite cuando no hay alquileres abiertos, o para `active` ⇄ `delinquent`, que lo define el frontend.

## Limitaciones del esquema actual

- No existe fecha real de devolución: `return_date_at` es la prevista, así que no se distingue una entrega tardía de una a tiempo. Para auditar `overdue` haría falta una columna como `returned_at`.
- No hay datos de pagos ni deuda: la BD no puede verificar la morosidad; se confía en lo que envía el frontend.
- Los `FK` tienen `ON DELETE NO ACTION`: no se puede borrar un auto o usuario con alquileres, sin importar el estado.
- Los estados no están restringidos por `CHECK`/`ENUM` en la BD (ver sección Estados).

## Diseño técnico propuesto para los cambios de estado

Decisión: máquina de estados declarativa. Las reglas son datos (YAML) y un motor genérico las ejecuta. No usar cadenas de `if` ni consultas dispersas por rutas o scripts. Aún no está implementado.

### Qué va en configuración y qué en código

| `config/status_transitions.yaml` (versionado en git) | Código Python (`services/`) |
|---|---|
| Estados de cada entidad | Funciones de guards (condiciones) y efectos (cambios en otras tablas) |
| Transiciones permitidas | Registro nombre → función (decoradores `@guard` / `@effect`) |
| Guards y efectos de cada transición, por nombre | Motor genérico (`state_machine.py`) |

Convención de nombres: `status` para todo lo que toca datos (columnas, YAML, `change_status`, `status_history`); `state machine` solo como nombre del patrón (`state_machine.py`).

Ejemplo de estructura (`car_rental`):

```yaml
car_rental:
  states: [pending, active, completed, cancelled, overdue]
  transitions:
    - from: null            # creación: el registro aún no existe
      to: pending
      guards: [user_is_active, car_is_available, return_after_rental]
      effects: [car_to_reserved]
    - from: pending
      to: active
      guards: [user_is_active, car_is_reserved]
      effects: [car_to_rented]
    - from: active
      to: completed
      guards: [car_is_rented]
      effects: [car_to_available]
```

Una transición que no aparece en el YAML queda prohibida. No hay que listar las inválidas.

La creación de un registro se modela como una transición con `from: null`, para que pase por los mismos guards y efectos. Solo se permite `from: null` hacia el estado inicial de la entidad.

### Reglas de implementación

- Formato YAML con el paquete `pyyaml` (nueva dependencia del `.venv`). Cargar siempre con `yaml.safe_load()`, nunca `yaml.load()`.
- Validar al arrancar y fallar rápido si: un guard o efecto no existe en el registro, una transición usa un estado no declarado, o hay estados duplicados.
- La config se aplica al reiniciar la app (con `debug=True`, Flask reinicia al cambiar archivos del proyecto). Una recarga en caliente solo se justifica si hace falta, y debe reemplazar la tabla únicamente después de validar el archivo nuevo.
- Una regla nueva que necesite un guard o efecto inexistente requiere programar la función y registrarla. Recombinar piezas existentes solo requiere editar el YAML.
- Un `StrEnum` por entidad como fuente única de los nombres de estado en Python.

### Dónde vive cada pieza

- Motor y registro: `services/state_machine.py`. Es lógica de negocio que orquesta varios repositorios dentro de una transacción; no va en `repositories/` ni en `routes/`.
- YAML: `config/status_transitions.yaml`, fuera del código. La ruta se calcula relativa al proyecto o se toma de una variable de entorno, para no depender del directorio de ejecución.
- Guards y efectos: un módulo `*_rules.py` por entidad, con guards y efectos juntos (se dividen solo si el archivo crece).
- Criterio de pertenencia: cada función va en el módulo de la **entidad dueña de la transición**, no de la entidad afectada. Ejemplo: `car_to_rented` se dispara desde un alquiler, así que vive en `car_rental_rules.py`. Así todo el flujo de una entidad se lee en un archivo y una sección del YAML.
- Funciones usadas por varias entidades: se importan desde el módulo de su dueño. Solo si no tienen dueño claro se crea `shared_rules.py`; no crearlo de antemano.

### Reglas de dependencia

- `routes/` solo llama a los servicios por entidad; nunca al motor, repositorios ni BD.
- Los servicios por entidad solo invocan el motor (`change_status` / `create`).
- Guards y efectos usan los repositorios, nunca la conexión; `db.py` sigue siendo el único archivo que la maneja.
- El motor no importa nada de Flask (se prueba sin servidor).
- Los repositorios no conocen el motor ni las reglas de estado.
- `services/` es la única capa que abre transacciones (`db.transaction()`). Los repositorios no controlan `commit` ni `rollback`.

### Registro con decoradores

Cada función se registra por nombre al definirla, y el motor la busca por el nombre que aparece en el YAML:

```python
@guard("user_is_active")
def user_is_active(ctx): ...

@effect("car_to_rented")
def car_to_rented(ctx): ...
```

- El decorador guarda la función en `GUARDS` / `EFFECTS` y la devuelve intacta. Si el nombre ya existe, lanza error (evita que una función pise a otra).
- **El registro ocurre al importar el módulo.** Los `*_rules.py` deben importarse antes de cargar el YAML; si no, el registro queda vacío y la validación falla.
- Orden de arranque: 1) importar los `*_rules.py`; 2) cargar el YAML; 3) validar que cada nombre exista en el registro; 4) construir la tabla de transiciones.
- Guards y efectos reciben un objeto de contexto (`Context`) con el registro actual, el estado destino y los repositorios. Un guard que falla lanza `BusinessRuleError`; un efecto modifica otras tablas a través de los repositorios.

### Flujo del motor (`change_status(entity, id, target)` y `create(entity, data)`)

1. Abrir transacción (`with db.transaction():`) y bloquear el registro con `SELECT ... FOR UPDATE` (en la creación se bloquean los registros relacionados, por ejemplo el auto y el usuario). Los repositorios comparten el `PgManager`, así que sus consultas quedan dentro de la transacción.
2. Buscar `(estado_actual, destino)` en la tabla de transiciones; en la creación, `(null, estado_inicial)`. Si no está, rechazar.
3. Ejecutar los guards en orden. Si uno falla, rechazar con su mensaje.
4. Hacer el `UPDATE` del estado (o el `INSERT` en la creación).
5. Ejecutar los efectos sobre las otras tablas, en la misma transacción.
6. Registrar el cambio en el historial y hacer `commit`. Cualquier fallo hace `rollback`.

### Piezas de apoyo

- Transacciones en `infrastructure/db.py` (único archivo que maneja la conexión), sobre la conexión única actual:
  - Hoy `execute_query` hace `commit()` en cada llamada y su `rollback()` solo cubre la consulta que falló; por eso no se pueden agrupar consultas en una operación atómica.
  - `PgManager` agrega `transaction()`, un context manager con un contador de profundidad (`_depth`, 0 = sin transacción). `execute_query` solo hace `commit()` cuando `_depth == 0`. Al salir del bloque, `transaction()` hace `commit` si todo salió bien o `rollback` si hubo una excepción; solo el bloque más externo confirma o revierte.
  - Los repositorios siguen recibiendo el `PgManager`; no hace falta un objeto `Transaction`.
  - Limitación: hay una sola conexión y un solo cursor compartidos. Flask atiende peticiones en varios hilos, así que dos peticiones podrían mezclar consultas dentro de una misma transacción. Mitigación mínima: un `threading.RLock` que adquieren `transaction()` y `execute_query`, lo que serializa el acceso a la BD.
  - `PgManager.from_env()` es un `@classmethod` (constructor alternativo) que lee las variables de entorno y devuelve un `PgManager`. `load_dotenv()` se llama una sola vez, en `app.py`, antes de construirlo. Las credenciales no van en el código.
- Mejora posterior (cuando el curso lo cubra): pool de conexiones.
  - `psycopg2.pool.ThreadedConnectionPool` creado al arrancar, con `minconn`/`maxconn` desde `DB_POOL_MIN`/`DB_POOL_MAX`; `transaction()` toma una conexión del pool y entrega un objeto `Transaction` con su propio `execute_query`, y siempre la devuelve (`putconn` en `finally`; si quedó rota, `close=True`). Los repositorios se instanciarían por transacción (`CarRepository(tx)`).
  - Si el pool se agota, `PoolError` (no espera): traducirlo a un error propio (HTTP 503) y dimensionar `maxconn` según los hilos y `max_connections` de PostgreSQL.
  - Hay un borrador en `infrastructure/db_new.py` (sin uso). El motor y los repositorios no cambian porque solo dependen de `execute_query`.
- Quién controla la transacción: `services/` (el motor) abre `with db.transaction():` porque una transacción equivale a una operación de negocio completa. Los repositorios solo ejecutan su SQL; nunca hacen `commit` ni `rollback`. Es la única excepción permitida a "nadie salta capas": `services/` usa `db.transaction()` de `infrastructure/`.
- No se anidan transacciones con intención; si hiciera falta, usar `SAVEPOINT`.
- Orden de bloqueo consistente: con `SELECT ... FOR UPDATE` en varias tablas, bloquear siempre en el mismo orden (`car_rental`, luego `car`, luego `user`) para evitar deadlocks. Ante `DeadlockDetected` o fallo de serialización, reintentar la transacción completa un número limitado de veces.
- Aislamiento: `READ COMMITTED` (por defecto) más `FOR UPDATE`; el índice único parcial cubre la carrera de dos alquileres abiertos por auto.
- Errores propios en `errors.py`, todos heredan de `AppError`. `routes/` los traduce una sola vez con manejadores de errores de Flask (`@app.errorhandler`): `NotFoundError` → 404, `InvalidTransitionError` → 409, `BusinessRuleError` → 422, `DatabaseUnavailableError` → 503; cualquier otro error → 500 y se registra con `logging`. No se pone `try/except` en cada ruta.
- Manejo de excepciones: capturar solo cuando se hace algo útil con el error, no para imprimirlo y relanzarlo (*log and rethrow*, que duplica el registro en cada capa).
  - Legítimo: `transaction()` captura para hacer `rollback` y relanza; un repositorio o servicio captura para traducir un error técnico en uno del dominio (p. ej. la violación de `uq_car_open_rental` en `BusinessRuleError`); `finally` para liberar recursos.
  - Los guards y efectos dejan subir los errores de BD: si se captura uno dentro de `transaction()` y se continúa, PostgreSQL deja la transacción abortada y las consultas siguientes fallan.
  - Pendiente: los repositorios actuales hacen `try/except` con `print` y `raise`; es válido mientras tanto, y se puede quitar cuando exista el manejador central.
- Tabla `status_history(entity, entity_id, from_status, to_status, changed_at, changed_by, reason)` para trazabilidad.
- Pruebas unitarias de la tabla de transiciones (combinaciones válidas e inválidas) sin depender de Flask.
- Ajustes necesarios en los repositorios:
  - `update_status(id, status)` en cada repositorio. El `update` actual exige todos los campos (p. ej. `make`, `model`, `year` y `status` en `car`) y obligaría a leer y reescribir el registro solo para cambiar el estado.
  - Lectura con bloqueo: `get_by_id_for_update(id)` en cada repositorio, con su `SELECT ... FOR UPDATE` escrito completo (sin armar el SQL por concatenación), junto a `get_by_id`. Ambos comparten un helper `_first_or_raise(results, id)` que lanza `NotFoundError` si no hay resultados y, si los hay, devuelve el registro formateado. `FOR UPDATE` solo mantiene el bloqueo dentro de `with db.transaction():`. Con la conexión única y el `RLock` es redundante dentro de un solo proceso, pero protege con varios procesos y queda listo para el pool.
  - `NotFoundError` (de `errors.py`) en lugar del `IndexError` genérico que hoy lanza `get_by_id` al hacer `results[0]` con un `id` inexistente.
  - Quitar `status` del `update` genérico (o rechazarlo si viene en los datos), para que el estado solo cambie por `update_status`, que solo llama el motor.
- La columna de estado es `account_status` en `user` y `status` en `car` y `car_rental`. No se renombra; el motor la resuelve con un mapeo por entidad.

### Defensa en la BD (última línea)

- `CHECK (status IN (...))` o tabla catálogo con `FK`, para impedir estados inventados.
- Índice único parcial para garantizar un solo alquiler abierto por auto, también con concurrencia:
  ```sql
  CREATE UNIQUE INDEX uq_car_open_rental ON lyfter_car_rental.car_rental (car_id)
  WHERE status IN ('pending','active','overdue');
  ```
- Opcional: tabla `status_transition(entity, from_status, to_status)` más trigger, generada a partir del YAML para no mantener dos listas a mano. No es prioritaria.

### Orden de implementación sugerido

1. `errors.py`, `transaction()` y `from_env()` en `infrastructure/db.py` (más `.env` y creación de `PgManager` en `app.py`); ajustes de los repositorios (`update_status`, `get_by_id_for_update`, `NotFoundError`). El pool de conexiones queda como mejora posterior, al final de la lista.
2. Enums, archivo `config/status_transitions.yaml`, y su carga y validación.
3. `services/state_machine.py` con el registro y el motor (`change_status` y `create`).
4. `car_rental_rules.py` y `car_rental_service.py`, porque `car_rental` dirige a las otras entidades.
5. Reglas y servicios de `car` y `user`.
6. Restricciones en la BD e historial de cambios.
7. Rutas Flask que llaman a los servicios y traducen los errores.
8. Mejora posterior: pool de conexiones y `Transaction` (ver "Piezas de apoyo").

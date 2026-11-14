# Información técnica: ejercicio 3 (ORM con SQLAlchemy)

Guía para aprender, explicar y reutilizar la solución. Está escrita paso a paso y asume que eres principiante. Todos los ejemplos de código salen del proyecto real.

## Índice

1. [Qué problema resuelve el proyecto](#1-qué-problema-resuelve-el-proyecto)
2. [Conceptos previos](#2-conceptos-previos)
3. [Mapa general: la arquitectura en capas](#3-mapa-general-la-arquitectura-en-capas)
4. [Estructura de carpetas](#4-estructura-de-carpetas)
5. [Capa por capa, paso a paso](#5-capa-por-capa-paso-a-paso)
6. [Recorrido completo de una operación](#6-recorrido-completo-de-una-operación)
7. [Resumen de patrones de diseño](#7-resumen-de-patrones-de-diseño)
8. [Principios SOLID en esta solución](#8-principios-solid-en-esta-solución)
9. [Decisiones técnicas importantes y su porqué](#9-decisiones-técnicas-importantes-y-su-porqué)
10. [Cómo aplicarlo a un proyecto nuevo](#10-cómo-aplicarlo-a-un-proyecto-nuevo)
11. [Limitaciones conocidas](#11-limitaciones-conocidas)
12. [Glosario](#12-glosario)

---

## 1. Qué problema resuelve el proyecto

El ejercicio pide manejar tres entidades (usuarios, carros y direcciones) guardadas en PostgreSQL, con estas operaciones:

- Crear, modificar y eliminar un usuario, un carro y una dirección.
- Asociar un carro a un usuario.
- Consultar todos los usuarios, carros y direcciones.

Las relaciones entre las entidades son:

```
User 1 ───── N Address     (un usuario tiene muchas direcciones)
User N ───── M Car         (un usuario puede tener muchos carros y un carro puede ser de muchos usuarios)
```

Una solución simple habría puesto todo en un solo archivo, con SQL mezclado con la lógica y la impresión en pantalla. Eso funciona para 20 líneas, pero se vuelve inmanejable al crecer. Este proyecto resuelve el mismo problema separando responsabilidades en capas, para que cada pieza sea pequeña, entendible y reemplazable.

---

## 2. Conceptos previos

### 2.1 ¿Qué es un ORM?

ORM significa *Object-Relational Mapper*. Traduce entre dos mundos:

| Base de datos (relacional) | Python (objetos) |
|---|---|
| Tabla `car` | Clase `Car` |
| Fila de la tabla | Objeto `Car(...)` |
| Columna `plate` | Atributo `car.plate` |
| Clave foránea | Relación `user.cars` |

Con un ORM trabajas con objetos y SQLAlchemy genera el SQL. Aquí se usa **SQLAlchemy 2.x** en su estilo declarativo (`Mapped[...]` y `mapped_column`).

### 2.2 Sesión (`Session`)

La `Session` es la "conversación" con la base de datos. Lleva el registro de qué objetos cargaste, creaste o modificaste y los envía a la BD cuando corresponde. Hay tres operaciones que debes distinguir:

| Operación | Qué hace |
|---|---|
| `add(obj)` | Marca el objeto para guardarse. Todavía no toca la BD. |
| `flush()` | Envía el SQL a la BD **dentro de la transacción**, pero todavía se puede deshacer. Aquí la BD valida restricciones (PK, unique, FK) y asigna los ids autogenerados. |
| `commit()` | Confirma la transacción. Los cambios quedan permanentes. |
| `rollback()` | Deshace todo lo que pasó desde el último commit. |

Esta diferencia es la base de todo el diseño: **los repositorios hacen `flush()` y quien controla la transacción hace `commit()`**.

### 2.3 Transacción

Un grupo de operaciones que se ejecutan todas o ninguna. Si en medio algo falla, se hace `rollback()` y la base de datos queda como estaba.

### 2.4 Restricción (constraint)

Una regla que la base de datos hace cumplir: llave primaria (`PRIMARY KEY`), valor único (`UNIQUE`), llave foránea (`FOREIGN KEY`), `NOT NULL`. Si la violas, PostgreSQL rechaza la operación y SQLAlchemy lanza `IntegrityError`.

### 2.5 DTO (Data Transfer Object)

Un objeto simple cuyo único trabajo es **transportar datos** entre capas. No tiene lógica de negocio ni acceso a la BD. Aquí se implementan con Pydantic.

---

## 3. Mapa general: la arquitectura en capas

Es una **arquitectura en capas** (*Layered Architecture*). Cada capa solo conoce a la que tiene debajo:

```
┌──────────────────────────────────────────────┐
│  app.py            (composition root + demo) │  ← quien arma todo y lo usa
├──────────────────────────────────────────────┤
│  services/         (casos de uso)            │  ← "qué se hace"
├──────────────────────────────────────────────┤
│  repositories/unit_of_work.py                │  ← controla la transacción
├──────────────────────────────────────────────┤
│  repositories/     (acceso a datos)          │  ← "cómo se guarda y se lee"
├──────────────────────────────────────────────┤
│  models/           (tablas como clases)      │
├──────────────────────────────────────────────┤
│  infrastructure/db.py  (Base + sesión)       │
└──────────────────────────────────────────────┘
        dtos/  y  exceptions.py  los usan todas las capas
```

**Por qué se hizo así:**

- **Cada capa tiene una sola razón para cambiar.** Si cambias de PostgreSQL a otra BD, tocas `db.py` y repositorios, no los servicios. Si cambias las reglas de negocio, tocas servicios, no los modelos.
- **Se puede probar y entender por partes.**
- **La dependencia va en una sola dirección** (de arriba hacia abajo). Nunca un modelo importa un servicio.

---

## 4. Estructura de carpetas

```
ejercicio3/
├── app.py                      # punto de entrada: arma las piezas y corre el demo
├── exceptions.py               # errores propios del dominio
├── infrastructure/
│   └── db.py                   # Base declarativa y fábrica de sesiones
├── models/
│   ├── user_model.py           # clase User  → tabla "user"
│   ├── car_model.py            # clase Car   → tabla "car"
│   ├── address_model.py        # clase Address → tabla "address"
│   └── user_car_model.py       # tabla de asociación "user_car"
├── repositories/
│   ├── base_repository.py      # CRUD genérico reutilizable
│   ├── user_repository.py
│   ├── car_repository.py
│   ├── address_repository.py
│   └── unit_of_work.py         # agrupa repositorios + sesión + transacción
├── services/
│   ├── user_service.py
│   ├── car_service.py
│   └── address_service.py
└── dtos/
    ├── read_base_dto.py        # base para DTOs de lectura
    ├── input_base_dto.py       # base para DTOs de entrada
    ├── user_dto.py, car_dto.py, address_dto.py
```

Regla de organización: **un archivo por entidad en cada capa**. Así sabes siempre dónde buscar.

---

## 5. Capa por capa, paso a paso

### 5.1 `infrastructure/db.py`: la base de todo

```python
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

def create_session_factory(database_url: str) -> sessionmaker:
    engine: Engine = create_engine(database_url, pool_pre_ping=True)
    return sessionmaker(engine, expire_on_commit=False)
```

**Qué hace cada parte**

1. **`Base`**: la clase madre de todos los modelos. Cuando una clase hereda de `Base`, SQLAlchemy sabe que representa una tabla.
2. **`NAMING_CONVENTION`**: obliga a que las restricciones tengan nombres predecibles (`uq_car_plate`, `pk_user`...). Sin esto, PostgreSQL inventa nombres aleatorios y es difícil referirse a ellos después (por ejemplo, en migraciones).
3. **`create_session_factory(url)`**: devuelve una **fábrica** de sesiones. Una fábrica es algo que, cada vez que lo llamas, te entrega una sesión nueva.
   - `pool_pre_ping=True`: antes de reusar una conexión, verifica que siga viva. Evita errores por conexiones caducadas.
   - `expire_on_commit=False`: **muy importante**. Por defecto, SQLAlchemy "caduca" los objetos después del `commit`, y si los lees después intenta ir a la BD otra vez. Aquí los servicios convierten el objeto a DTO después del commit, así que se desactiva.

**Patrón: Factory (fábrica).** La función recibe la URL y construye los objetos complejos. **Por qué no se crea el engine al importar el archivo:** si se hiciera, la conexión se configuraría antes de que `load_dotenv()` cargue el `.env`, y el código no sería testeable ni configurable. Ahora quien llama decide cuándo y con qué URL.

---

### 5.2 `models/`: las tablas como clases

```python
class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    users: Mapped[list["User"]] = relationship(
        secondary="user_car",
        back_populates="cars"
    )
```

**Cómo leerlo**

- `Mapped[int]` es el tipo en Python. `mapped_column(...)` define cómo es la columna en la BD.
- `primary_key=True` sobre un entero hace que **PostgreSQL genere el número automáticamente** (autonumérico). Por eso nunca enviamos un `id` al crear.
- `unique=True` en `plate` crea la restricción `uq_car_plate`: no puede haber dos carros con la misma placa.
- `nullable=False` equivale a `NOT NULL`.

**Relaciones**

| Relación | Cómo se define | Detalle |
|---|---|---|
| `User` 1 ─ N `Address` | `User.addresses` / `Address.user` | `Address` tiene la FK `user_id`. `back_populates` hace que ambos lados se mantengan sincronizados. |
| `User` N ─ M `Car` | `secondary=user_car` | Una relación muchos a muchos **necesita una tabla intermedia** (`user_car`) con dos llaves foráneas. |

```python
user_car = Table(
    "user_car", Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("car_id",  ForeignKey("car.id"),  primary_key=True),
)
```

Las dos columnas juntas son la llave primaria (**llave compuesta**). Esto impide asociar el mismo carro al mismo usuario dos veces.

**`cascade="all, delete-orphan"`** en `User.addresses`: al borrar un usuario, se borran sus direcciones. Una dirección sin usuario no tiene sentido en este modelo. En cambio, entre usuario y carro no hay cascada: borrar un usuario no borra los carros, solo las filas de asociación.

**`TYPE_CHECKING` y strings como `"User"`**: `user_model` necesita conocer `Car` y `car_model` necesita conocer `User`. Si cada uno importara al otro directamente, tendrías un **import circular** (A importa B que importa A) y Python fallaría. La solución es importar solo para los tipos (`if TYPE_CHECKING:`) y referirse a la clase por nombre en texto.

**`models/__init__.py`** importa todos los modelos para que SQLAlchemy los registre antes de usarlos.

**Patrón: Data Mapper.** El modelo describe la estructura y la persistencia la hace la `Session`, no el propio objeto. (Lo contrario sería *Active Record*, donde el objeto se guarda a sí mismo con `car.save()`.)

---

### 5.3 `exceptions.py`: errores propios

```python
class NotFoundError(Exception): ...
class InvalidFieldError(Exception): ...
class ConflictError(Exception): ...
```

| Excepción | Cuándo se lanza |
|---|---|
| `NotFoundError` | Se busca un registro por id y no existe. |
| `InvalidFieldError` | Se intenta modificar un campo que no está permitido. |
| `ConflictError` | La BD rechaza el registro por duplicado (llave primaria o único). |

**Por qué se crean propias en vez de dejar pasar las de SQLAlchemy:** `IntegrityError` es un detalle de la librería. Si las capas superiores la conocieran, estarían acopladas a SQLAlchemy y, si algún día cambias de librería, tendrías que tocar todo. Con errores propios, las capas altas hablan el lenguaje del problema ("conflicto", "no encontrado") y no el de la herramienta.

**Patrón: Exception Translation (traducción de excepciones).** Se captura el error técnico en el borde de la capa y se relanza como error de dominio.

---

### 5.4 `dtos/`: los datos que viajan entre capas

Los DTOs usan **Pydantic v2**, que valida tipos automáticamente (por ejemplo `EmailStr` rechaza correos mal formados).

Hay **dos clases base** donde se centraliza la configuración:

```python
class ReadBaseDTO(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)

class InputBaseDTO(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True, extra="forbid")
```

| Opción | Efecto |
|---|---|
| `frozen=True` | El DTO es inmutable: una vez creado no se modifica. Evita errores sutiles. |
| `from_attributes=True` | Permite construir el DTO directamente desde un objeto ORM (`model_validate(obj)`). |
| `str_strip_whitespace=True` | Quita espacios sobrantes en los textos recibidos. |
| `extra="forbid"` | Si llega un campo que no existe en el DTO, se rechaza (protege contra datos inventados). |

**Tipos de DTO por entidad** (ejemplo con `Car`):

| DTO | Para qué | Hereda de |
|---|---|---|
| `CarDTO` | Lo que **sale** (lectura): incluye `id`. | `ReadBaseDTO` |
| `CarCreateDTO` | Lo que **entra** al crear: **no lleva `id`**, lo genera la BD. | `InputBaseDTO` |
| `CarUpdateDTO` | Lo que entra al modificar: todos los campos opcionales (`T \| None = None`). | `InputBaseDTO` |
| `UserReadDTO` | Solo existe para `User`: agrega `cars` y `addresses` anidados. | `UserDTO` |

**Por qué se separan Create / Update / Read** (en vez de un único `CarDTO`):

- Al crear no existe `id`; al leer sí.
- Al actualizar solo envías lo que cambia.
- Así cada operación expone exactamente los campos que le corresponden.

**Por qué los DTOs y no devolver los objetos ORM directamente:** un objeto ORM está "pegado" a la sesión. Si la sesión se cierra y accedes a una relación no cargada, SQLAlchemy lanza `DetachedInstanceError`. El DTO es una copia simple de los datos, segura para pasar a cualquier lugar. Además, las capas superiores no necesitan saber que existe SQLAlchemy.

**Relaciones anidadas en un solo sentido:** `UserReadDTO` contiene `cars: list[CarDTO]`, pero `CarDTO` **no** contiene usuarios. Si ambos se contuvieran mutuamente se produciría una recursión infinita.

**Patrón: DTO.**

---

### 5.5 `repositories/base_repository.py`: el CRUD genérico

Esta es la pieza más reutilizable del proyecto.

```python
class BaseRepository(Generic[T]):
    model: ClassVar[type[T]]
    updatable: ClassVar[frozenset[str]] = frozenset()
    load_options: ClassVar[tuple] = ()

    def __init__(self, session: Session):
        self._session = session
```

**Idea clave:** en vez de escribir `create`, `update`, `delete`, `get_all` y `get_by_id` tres veces (una por entidad), se escriben **una sola vez** y cada repositorio concreto solo declara su configuración:

```python
class CarRepository(BaseRepository[Car]):
    model = Car
    updatable = frozenset({"plate", "make", "model", "year"})
    load_options = (selectinload(Car.users),)
```

- **`Generic[T]`**: indica que la clase funciona con "algún modelo T". Aquí `BaseRepository[Car]` le dice a Python y al editor que devuelve objetos `Car`.
- **`model`**: qué clase de modelo maneja.
- **`updatable`**: lista blanca de campos que se permiten modificar. Si intentas cambiar otro, se lanza `InvalidFieldError`. Protege campos sensibles como el `id`.
- **`load_options`**: instrucciones de carga de relaciones (ver abajo).

**Los cinco métodos:**

```python
def get_by_id(self, entity_id):
    entity = self._session.get(self.model, entity_id, options=self.load_options)
    if entity is None:
        raise NotFoundError(...)
    return entity
```
Busca por llave primaria y, si no existe, lanza `NotFoundError` (así quien llama nunca recibe `None` por sorpresa).

```python
def create(self, **data):
    entity = self.model(**data)
    self._session.add(entity)
    try:
        self._session.flush()
    except IntegrityError as e:
        raise ConflictError(f"{self.model.__name__} duplicado.") from e
    return entity
```
Crea el objeto, lo agrega y hace `flush()`. En el `flush` la BD valida las restricciones: si hay duplicado, se traduce a `ConflictError`. `from e` conserva el error original para depuración.

```python
def update(self, entity_id, **data):
    invalid = data.keys() - self.updatable
    if invalid:
        raise InvalidFieldError(...)
    entity = self.get_by_id(entity_id)
    for field, value in data.items():
        setattr(entity, field, value)
    self._session.flush()
    return entity
```
Primero valida los campos contra la lista blanca, luego carga la entidad y asigna los nuevos valores.

`delete` y `get_all` siguen la misma lógica.

**`**data: Any`**: recibir `**kwargs` permite que el repositorio sea genérico y no nombre ningún campo. Cualquier modelo puede pasar sus propios datos.

**Eager loading con `selectinload`:** las relaciones se cargan "perezosamente" por defecto (solo cuando las lees). Pero con la sesión ya cerrada eso fallaría. `selectinload` le dice a SQLAlchemy: "cuando cargues un `User`, trae también sus `cars` y `addresses` en una consulta adicional". Se usa `selectinload` (y no un `JOIN`) porque para colecciones evita multiplicar filas.

**Patrones: Repository + Generic Repository.**
- **Repository**: esconde *cómo* se accede a los datos detrás de una interfaz parecida a una colección (`get_all`, `create`...). Las capas superiores no escriben consultas.
- **Template por configuración (variables de clase)**: el comportamiento común está en la base y cada subclase solo personaliza con `model`, `updatable` y `load_options`. Es una variante simple y muy legible del patrón *Template Method*.

**Importante:** los repositorios solo hacen `flush()`, nunca `commit()`. Quien decide si confirmar o deshacer es la Unit of Work.

---

### 5.6 `UserRepository`: operaciones propias de una relación

```python
class UserRepository(BaseRepository[User]):
    model = User
    updatable = frozenset({"name", "full_name"})
    load_options = (selectinload(User.addresses), selectinload(User.cars))

    def __init__(self, session):
        super().__init__(session)
        self._cars = CarRepository(session)

    def associate_car(self, user_id, car_id):
        user = self.get_by_id(user_id)
        car = self._cars.get_by_id(car_id)
        if car not in user.cars:
            user.cars.append(car)
            self._session.flush()
        return user
```

- Hereda todo el CRUD gratis y agrega lo específico: asociar y desasociar carros.
- Usa un `CarRepository` **con la misma sesión**, así todo ocurre en la misma transacción.
- `associate_car` recibe **ids**, no objetos: quien llama no necesita cargar entidades. El repositorio las resuelve (y lanza `NotFoundError` si alguna no existe).
- `if car not in user.cars` hace la operación **idempotente**: asociar dos veces no duplica ni da error.
- `user.cars.append(car)` es todo lo que se necesita: SQLAlchemy genera el `INSERT` en la tabla `user_car` por sí solo.

---

### 5.7 `repositories/unit_of_work.py`: la transacción

```python
class UnitOfWork:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self._session = None

    def __enter__(self):
        self._session = self._session_factory()
        self.addresses = AddressRepository(self._session)
        self.cars = CarRepository(self._session)
        self.users = UserRepository(self._session)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is not None:
                self._session.rollback()
        finally:
            self._session.close()

    def commit(self):
        self._session.commit()
```

**El problema que resuelve:** una operación de negocio puede tocar varios repositorios (por ejemplo, crear una dirección verifica el usuario y luego guarda la dirección). Todos deben compartir **la misma sesión y la misma transacción**, y alguien debe encargarse de confirmar o deshacer. Eso es la Unit of Work.

**Cómo funciona con `with`:**

```python
with uow_factory() as uow:       # __enter__: abre sesión, crea repositorios
    uow.users.create(...)        # trabaja
    uow.commit()                 # confirma
                                 # __exit__: si hubo error → rollback; siempre → close
```

- Si ocurre cualquier excepción dentro del bloque, `__exit__` recibe el error y hace `rollback()`. La BD no queda a medias.
- El `finally` garantiza que la sesión **siempre se cierre**, pase lo que pase.
- El `commit()` es **explícito**: solo se confirma si el servicio llegó hasta ahí.

**Patrones:**
- **Unit of Work**: mantiene los cambios de una operación de negocio juntos y los confirma o deshace como una unidad.
- **Context Manager**: el protocolo `with` (`__enter__` / `__exit__`) garantiza la limpieza de recursos sin que tengas que acordarte de cerrar nada.

---

### 5.8 `services/`: los casos de uso

```python
class CarService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def create_car(self, data: CarCreateDTO) -> CarDTO:
        with self._uow_factory() as uow:
            car = uow.cars.create(**data.model_dump())
            uow.commit()
            return CarDTO.model_validate(car)
```

Cada método de servicio sigue **exactamente el mismo molde**:

1. Abrir una Unit of Work (`with self._uow_factory() as uow`).
2. Llamar a los repositorios necesarios.
3. `uow.commit()` si hubo cambios.
4. Convertir el resultado a DTO **dentro del `with`** y devolverlo.

**Detalles que importan**

- **`**data.model_dump()`**: convierte el DTO en un diccionario y lo pasa como argumentos al repositorio. El servicio no nombra ningún campo, así que agregar un campo no obliga a modificarlo.
- **`model_dump(exclude_unset=True)` en las actualizaciones**: solo incluye los campos que el llamador realmente envió. Sin esto, un campo no enviado llegaría como `None` y borraría el dato existente. Así se permite la modificación **parcial**.
- **Reciben y devuelven DTOs**, nunca objetos ORM. Las capas superiores no saben que existe SQLAlchemy.
- **Validación de dependencias:** `create_address` primero hace `uow.users.get_by_id(data.user_id)`. Si el usuario no existe se lanza `NotFoundError` con un mensaje claro, en lugar de un error técnico de llave foránea.
- **`UserService.get_all`** devuelve `UserReadDTO` (con carros y direcciones) y `get_by_id` devuelve el `UserDTO` plano.

**Qué NO hace el servicio:** no escribe SQL, no conoce sesiones y no hace `rollback` (lo hace el `__exit__` de la UoW).

**Patrones:**
- **Service Layer**: concentra los casos de uso ("crear un carro", "asociar un carro a un usuario") en un solo lugar, entre quien los pide y el acceso a datos.
- **Dependency Injection (inyección de dependencias)**: el servicio **recibe** su fábrica de UoW por el constructor en lugar de crearla él mismo. Así puedes darle otra distinta (por ejemplo, una de pruebas).

---

### 5.9 `app.py`: donde todo se conecta

```python
def build_car_service() -> CarService:
    session_factory = create_session_factory(get_database_url())
    return CarService(partial(UnitOfWork, session_factory))
```

**Cómo se arma la cadena**

1. `get_database_url()` lee `DATABASE_URL` del entorno (y falla con un mensaje claro si falta).
2. `create_session_factory(url)` crea la fábrica de sesiones.
3. `partial(UnitOfWork, session_factory)` crea una "mini-fábrica": cada vez que se llame sin argumentos, produce un `UnitOfWork` ya configurado con esa fábrica de sesiones. Es el `Callable[[], UnitOfWork]` que espera el servicio.
4. `CarService(...)` recibe esa fábrica.

**`main()`** carga el `.env`, configura el logging, construye los tres servicios y ejecuta el demo dentro de un `try/except` que traduce los errores de dominio a mensajes legibles:

```python
except ValidationError as ve:                                  # Pydantic
    logger.error(f"Datos inválidos: {ve}")
except (NotFoundError, InvalidFieldError, ConflictError) as e: # dominio
    logger.error(f"Operación rechazada: {e}")
except Exception as e:                                         # lo inesperado
    logger.error(f"Excepcion general: {e}")
```

El orden importa: de lo más específico a lo más general.

**Patrón: Composition Root.** Es **el único lugar** donde se crean y conectan las dependencias concretas. El resto del código solo recibe lo que necesita. Si quieres cambiar una implementación, lo haces aquí.

---

## 6. Recorrido completo de una operación

Seguimos `service.create_car(CarCreateDTO(plate="123456", make="Toyota", model="Yaris", year=2010))`:

```
 1. app.py            Crea el CarCreateDTO. Pydantic valida tipos y rechaza campos extra.
 2. CarService        Llama create_car(data).
 3. CarService        Abre `with self._uow_factory() as uow`.
 4. UnitOfWork        __enter__: crea Session + AddressRepository, CarRepository, UserRepository.
 5. CarService        data.model_dump() → {"plate": "123456", "make": "Toyota", ...}
 6. BaseRepository    create(**data): Car(**data), session.add(), session.flush().
 7. PostgreSQL        Ejecuta INSERT, valida PK y unique(plate), genera el id.
       ├─ Si la placa ya existe → IntegrityError
       │     └─ BaseRepository la traduce a ConflictError
       │         └─ Sube por el `with` → UnitOfWork.__exit__ hace rollback() y close()
       │             └─ app.py la captura: "Operación rechazada: Car duplicado."
       └─ Si todo está bien → continúa
 8. CarService        uow.commit() → la transacción se confirma.
 9. CarService        CarDTO.model_validate(car) → copia los datos del objeto a un DTO.
10. UnitOfWork        __exit__ sin error: solo close().
11. app.py            Recibe el CarDTO con el id ya asignado.
```

Fíjate en cómo cada capa hace **una sola cosa** y cómo el error de duplicado viaja hacia arriba convertido en un lenguaje que todas las capas entienden.

---

## 7. Resumen de patrones de diseño

| # | Patrón | Dónde está | Qué problema resuelve |
|---|---|---|---|
| 1 | **Layered Architecture** | Toda la estructura | Separa responsabilidades y fija la dirección de las dependencias. |
| 2 | **Repository** | `repositories/` | Oculta los detalles de acceso a datos detrás de una interfaz simple. |
| 3 | **Generic Repository** | `BaseRepository[T]` | Evita repetir el CRUD en cada entidad. |
| 4 | **Template Method (por variables de clase)** | `model`, `updatable`, `load_options` | La base define el algoritmo y las subclases solo lo configuran. |
| 5 | **Unit of Work** | `UnitOfWork` | Agrupa operaciones en una transacción única y coherente. |
| 6 | **Context Manager** | `__enter__`/`__exit__` | Garantiza rollback y cierre de la sesión aunque haya errores. |
| 7 | **Service Layer** | `services/` | Centraliza los casos de uso y la lógica de aplicación. |
| 8 | **DTO** | `dtos/` | Transporta datos de forma segura y desacopla las capas del ORM. |
| 9 | **Dependency Injection** | Constructores de servicios, UoW y repositorios | Reduce el acoplamiento y facilita las pruebas. |
| 10 | **Factory** | `create_session_factory`, `partial(UnitOfWork, ...)` | Centraliza la creación de objetos complejos. |
| 11 | **Composition Root** | `app.py` | Un único lugar donde se arman todas las dependencias. |
| 12 | **Data Mapper** | SQLAlchemy ORM + `models/` | Los objetos no saben cómo guardarse; lo hace la sesión. |
| 13 | **Exception Translation** | `create()` → `ConflictError` | Aísla las capas altas de los errores de la librería. |
| 14 | **Whitelist (lista blanca)** | `updatable` | Solo se pueden modificar los campos permitidos. |

Cómo se relacionan: la **Service Layer** usa la **Unit of Work**, que agrupa **Repositories**, que operan sobre modelos mapeados con **Data Mapper**. Todo se conecta por **Dependency Injection** en el **Composition Root**.

---

## 8. Principios SOLID en esta solución

| Principio | Cómo aparece |
|---|---|
| **S**: Responsabilidad única | Cada clase hace una cosa: el repositorio accede a datos, el servicio orquesta el caso de uso, la UoW maneja la transacción, el DTO transporta datos. |
| **O**: Abierto/cerrado | Para agregar una entidad nueva creas un modelo, un repositorio de 3 líneas y un servicio, **sin modificar** `BaseRepository` ni la UoW (salvo registrar el repositorio nuevo en esta última). |
| **L**: Sustitución de Liskov | Cualquier subclase de `BaseRepository` se puede usar donde se espera un repositorio base. |
| **I**: Segregación de interfaces | DTOs separados (Create/Update/Read): cada operación solo ve los campos que necesita. |
| **D**: Inversión de dependencias | Los servicios reciben su `uow_factory` por constructor en lugar de crear sus dependencias. (Mejora pendiente: tipar contra un `Protocol` en vez del `UnitOfWork` concreto; es la tarea #37 del TODO.) |

---

## 9. Decisiones técnicas importantes y su porqué

### 9.1 IDs autonuméricos generados por la BD

**Antes:** los DTOs de creación exigían `id` y el demo enviaba `id=12`. Al ejecutar dos veces, el segundo intento chocaba con la llave primaria ("llave duplicada").
**Ahora:** `id` es `primary_key=True` sin valor asignado, y PostgreSQL lo genera. Los `CreateDTO` no tienen `id`.
**Por qué:** el cliente no debe decidir identificadores, porque eso genera colisiones. Es la práctica estándar.

### 9.2 Duplicados: restricción en la BD + traducción del error (y no solo un `if` previo)

Una opción habría sido consultar "¿ya existe?" antes de insertar. Pero tiene un fallo: **condición de carrera**. Si dos procesos consultan al mismo tiempo, ambos ven "no existe" y ambos intentan insertar.
La única garantía real es la **restricción `UNIQUE`/`PRIMARY KEY` en la base de datos**. El código solo captura el `IntegrityError` y lo convierte en `ConflictError`. Se hace **una vez** en `BaseRepository.create`, y por eso los servicios no repiten esa verificación.

### 9.3 `flush()` en repositorios y `commit()` en la UoW

Si cada repositorio hiciera `commit()`, una operación que usa dos repositorios podría quedar a medias (la primera parte confirmada y la segunda fallida). Con `flush()` todo queda dentro de **una sola transacción**, y se confirma o se deshace en conjunto.

### 9.4 DTOs en lugar de objetos ORM

Evita `DetachedInstanceError`, desacopla las capas superiores de SQLAlchemy y permite controlar exactamente qué datos salen y entran.

### 9.5 Lista blanca `updatable`

Sin ella, un `update` con `id=999` o cualquier campo accidental modificaría datos que no debería. Rechazar campos desconocidos es más seguro que ignorarlos en silencio.

### 9.6 `model_dump(exclude_unset=True)`

Diferencia "no me enviaron este campo" de "me enviaron `None`". Así las actualizaciones parciales no borran datos.

### 9.7 Fábricas (`partial`) en vez de pasar un UoW ya creado

Cada llamada al servicio necesita su **propia** sesión y transacción. Si el servicio recibiera un único UoW, todas las operaciones compartirían estado. Pasar una fábrica garantiza una sesión limpia por operación.

### 9.8 `from e` al relanzar excepciones

`raise ConflictError(...) from e` conserva la causa original. En un error real puedes ver tanto el mensaje amigable como el `IntegrityError` técnico en el traceback.

### 9.9 Tipado (`Mapped`, `ClassVar`, `Generic`)

El código es autodocumentado y el editor te avisa de errores antes de ejecutar.

---

## 10. Cómo aplicarlo a un proyecto nuevo

Checklist para replicar este diseño con otras entidades (por ejemplo, `Product`):

1. **Modelo** (`models/product_model.py`): hereda de `Base`, define columnas y restricciones (`unique`, `nullable`). Importa el modelo en `models/__init__.py`.
2. **DTOs** (`dtos/product_dto.py`): `ProductDTO` (lectura, con `id`), `ProductCreateDTO` (sin `id`), `ProductUpdateDTO` (campos opcionales).
3. **Repositorio** (`repositories/product_repository.py`):
   ```python
   class ProductRepository(BaseRepository[Product]):
       model = Product
       updatable = frozenset({"name", "price"})
   ```
   Agrega `load_options` si tiene relaciones que necesites cargar.
4. **Unit of Work**: agrega `self.products = ProductRepository(self._session)` en `__enter__`.
5. **Servicio** (`services/product_service.py`): copia el molde (abrir UoW → repositorio → commit → DTO).
6. **Composición** (`app.py`): crea un `build_product_service()` igual a los demás.
7. **Errores**: captura `NotFoundError`, `ConflictError` e `InvalidFieldError` donde llames al servicio.

**Reglas para no perder el orden**

- Cada capa solo importa de la inmediatamente inferior.
- Los servicios no escriben consultas. Los repositorios no hacen `commit`.
- Nunca devuelvas objetos ORM fuera del servicio.
- Las restricciones de integridad van en la base de datos. El código las traduce, no las reemplaza.
- No uses ids enviados por el usuario como llave primaria.
- Los errores de librería (SQLAlchemy) se traducen a errores propios en la capa de repositorio.

**Cómo explicarlo en una entrevista (resumen de 30 segundos):**
"Usé arquitectura en capas. Los modelos mapean las tablas con SQLAlchemy. Un repositorio genérico encapsula el CRUD y traduce errores de la base de datos a excepciones de dominio. Una Unit of Work agrupa los repositorios en una sola transacción con un context manager. Los servicios implementan los casos de uso y trabajan solo con DTOs de Pydantic. Todo se conecta por inyección de dependencias en un Composition Root."

---

## 11. Limitaciones conocidas

Para entender dónde está el proyecto hoy (el detalle completo está en `TODO.md`):

- `update()` no traduce `IntegrityError`: cambiar una placa a una que ya existe lanzaría el error crudo de SQLAlchemy.
- No hay pruebas automáticas ni migraciones (el esquema se crea con `Ejercicio2_y_3_create_tables.py`, un script aparte que borra y recrea las tablas).
- El demo de `app.py` usa ids fijos en la asociación y desasociación, por lo que solo coincide con filas reales en un esquema recién creado.
- `disassociate_user_car` tiene un chequeo `is None` que nunca se cumple (porque `get_by_id` ya lanza `NotFoundError`).
- Hay imports sin usar (`address_service.py`, `db.py`) y una excepción sin uso (`ValidationError` en `exceptions.py`).
- Los servicios dependen del `UnitOfWork` concreto, no de una abstracción (`Protocol`).

---

## 12. Glosario

| Término | Significado |
|---|---|
| **ORM** | Herramienta que traduce entre objetos de Python y tablas de la base de datos. |
| **Modelo** | Clase que representa una tabla. |
| **Sesión** | La conexión de trabajo con la BD que registra los cambios pendientes. |
| **Transacción** | Conjunto de operaciones que se confirman o se deshacen juntas. |
| **flush / commit / rollback** | Enviar cambios a la BD sin confirmar / confirmar / deshacer. |
| **Llave primaria (PK)** | Identificador único de cada fila. |
| **Llave foránea (FK)** | Columna que apunta a la PK de otra tabla. |
| **IntegrityError** | Error de SQLAlchemy cuando se viola una restricción de la BD. |
| **Eager loading** | Cargar las relaciones por adelantado en vez de bajo demanda. |
| **DTO** | Objeto simple que solo transporta datos entre capas. |
| **Repositorio** | Clase que encapsula el acceso a los datos de una entidad. |
| **Unit of Work** | Objeto que agrupa varios repositorios en una sola transacción. |
| **Servicio** | Clase que implementa los casos de uso de la aplicación. |
| **Inyección de dependencias** | Entregar a un objeto lo que necesita en vez de que lo cree él mismo. |
| **Composition Root** | El punto único donde se construyen y conectan las dependencias. |
| **Context manager** | Objeto usable con `with` que garantiza la limpieza de recursos. |
| **Idempotente** | Operación que repetida produce el mismo resultado que ejecutada una vez. |
| **Condición de carrera** | Error que depende del orden en que se ejecutan procesos simultáneos. |

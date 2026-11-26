# Información técnica: Ejercicio de Authorization (Flask + SQLAlchemy)

Documento didáctico para repasar la solución: qué hace cada pieza, qué patrón se usó, qué problema resuelve y por qué se eligió.

---

## 1. Visión general

API REST en Flask con:

- CRUD de **productos** y **usuarios**.
- **Autenticación** con JWT firmado con RS256 (login, access token + refresh token).
- **Autorización** por roles (`admin`, `user`).
- **Refresh tokens con rotación** (refresh y logout).
- **Facturación**: facturas y detalles de factura (solo crear y leer).

### Conceptos base

| Concepto | Pregunta que responde | Ejemplo aquí |
|---|---|---|
| **Autenticación** | ¿Quién eres? | Login con usuario/contraseña → token |
| **Autorización** | ¿Qué puedes hacer? | Solo `admin` ve todas las facturas |

Códigos HTTP asociados:

- **401**: no sabemos quién eres (token ausente, inválido o expirado; credenciales malas).
- **403**: sabemos quién eres, pero tu rol no alcanza.

---

## 2. Arquitectura en capas

Un archivo por entidad, nombrado `<entidad>_<capa>.py`.

```
Request HTTP
    │
    ▼
routes/        → recibe HTTP, valida con DTOs, llama al servicio, devuelve JSON
    │
    ▼
services/      → lógica de negocio (qué significa cada caso de uso)
    │
    ▼
repositories/  → acceso a datos (SQLAlchemy), vía UnitOfWork
    │
    ▼
models/        → tablas (ORM)
```

| Capa | Responsabilidad | Lo que NO hace |
|---|---|---|
| `routes/` | Traducir HTTP ↔ llamadas al servicio | Lógica de negocio, SQL |
| `services/` | Reglas de negocio, orquestación | Conocer Flask, werkzeug o PyJWT |
| `repositories/` | Responder preguntas sobre datos | Decidir qué significa que algo no exista para un caso de uso |
| `models/` | Describir tablas y relaciones | Lógica |
| `dtos/` | Definir la forma de entrada/salida | Contener modelos ORM |

**Por qué capas:** cada una cambia por una razón distinta (Single Responsibility). Si mañana cambias de Flask a FastAPI, solo tocas `routes/`. Si cambias de base de datos, solo `repositories/` e `infrastructure/`.

Ejemplo de la separación repositorio/servicio: `get_by_username` lanza `NotFoundError` ("no hay dato"). Es el **servicio de autenticación** quien decide que eso, en un login, se convierte en `InvalidCredentialsError` ("usuario o contraseña incorrectos"). El repositorio no sabe de logins.

---

## 3. Principios SOLID aplicados

### S: Single Responsibility
- `UserService` hace CRUD de usuarios y **nunca emite tokens**; eso es de `AuthenticationService`.
- `JwtSigner` firma, `JwtVerifier` verifica: dos clases, dos razones de cambio.
- `AuthenticationGuard` solo protege rutas.

### O: Open/Closed
- Para añadir una entidad nueva (ej. facturas) se crean archivos nuevos (`invoice_model`, `invoice_repository`, `invoice_service`, `invoice_routes`) sin modificar la lógica de las existentes.
- Los roles son un `StrEnum`: añadir uno no obliga a reescribir los guards.

### L: Liskov Substitution
- Cualquier implementación de `PasswordHasher` (werkzeug, bcrypt, argon2) puede sustituir a otra sin que el servicio note la diferencia, porque respeta el contrato.

### I: Interface Segregation
- `TokenSigner` y `TokenVerifier` son protocolos **separados**. Quien solo verifica (el guard) no recibe la clave privada ni la capacidad de firmar.

### D: Dependency Inversion
- Los servicios dependen de **abstracciones** (`PasswordHasher`, `TokenSigner`, `TokenVerifier` en `services/protocols.py`), no de werkzeug ni PyJWT.
- Los detalles concretos viven en `infrastructure/`.

---

## 4. Patrones de diseño usados

### 4.1 Arquitectura hexagonal (Ports & Adapters)

- **Puertos**: los protocolos en `services/protocols.py`.
- **Adaptadores**: `WerkzeugPasswordHasher`, `JwtSigner`, `JwtVerifier` en `infrastructure/`.

**Qué resuelve:** que la lógica de negocio no quede atada a librerías externas.
**Por qué:** si PyJWT cambia o decides usar otra librería, escribes un adaptador nuevo y los servicios no se tocan. También facilita pruebas: se puede inyectar un hasher falso.

```python
# services/protocols.py (idea)
class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...
```

### 4.2 Inyección de dependencias + Composition Root

- `app.py` es el **único** lugar que conoce las clases concretas: lee `.env`, lee las claves, construye adaptadores, servicios y los inyecta hacia abajo.
- Las rutas se registran con `register_*_routes(app, service, guard)`: reciben sus dependencias, no las crean.

**Qué resuelve:** el acoplamiento. Nadie hace `JwtSigner(...)` dentro de un servicio.
**Por qué:** las dependencias son explícitas, intercambiables y fáciles de probar. Es la aplicación práctica de Dependency Inversion.

### 4.3 Repository

Cada entidad tiene un repositorio que encapsula las consultas SQLAlchemy.

**Qué resuelve:** que el servicio no escriba consultas ni conozca detalles del ORM.
**Por qué:** centraliza el acceso a datos; los repositorios comparten una base con `updatable` (columnas permitidas de actualizar) y `load_options` (qué relaciones cargar).

Detalles útiles:

- `InvoiceRepository.load_options = (selectinload(Invoice.invoice_details),)`: carga los detalles junto con la factura **antes de que se cierre la sesión**, evitando `DetachedInstanceError`.
- `updatable` es una lista blanca: solo esas columnas pueden modificarse (protege contra actualizar campos no deseados).

### 4.4 Unit of Work

`UnitOfWork` agrupa los repositorios (`uow.users`, `uow.products`, `uow.invoices`, `uow.refresh_tokens`) bajo **una sola sesión/transacción**. Se usa como `with uow_factory() as uow:`.

**Qué resuelve:** que varias operaciones se confirmen o se deshagan juntas.
**Por qué:** crear una factura implica leer productos y guardar factura + detalles; o todo se guarda o nada. `__exit__` hace commit si todo fue bien y rollback si hubo excepción.

Matiz importante (rotación de tokens): al detectar reutilización de un refresh token hay que revocar todos los tokens del usuario y **hacer commit antes de lanzar la excepción**, porque `__exit__` hace rollback ante cualquier excepción y se perdería la revocación.

### 4.5 DTO (Data Transfer Object)

Clases Pydantic que definen qué entra y qué sale por la API (`UserDTO`, `UserCreateDTO`, `InvoiceDTO`, `TokenDTO`…).

**Qué resuelve:** que el cliente no controle campos que no debe y que no se exponga información sensible.
**Por qué (seguridad):**

- `UserDTO` expone `role` pero **no** `password`.
- `UserCreateDTO`/`UserUpdateDTO` **no aceptan `role`**: nadie puede auto-promoverse a admin (evita *mass assignment* / escalada de privilegios).
- `InvoiceCreateDTO` no acepta `user_id` (sale del token), ni `total_amount`, `amount`, `price` (se calculan en el servidor; el cliente no es confiable).
- Los DTOs nunca incluyen modelos ORM; son la frontera de la API.
- Validaciones declarativas: `quantity` con `Field(gt=0)`, `invoice_details` con `Field(min_length=1)`, `max_length` igual al de la columna del modelo.

### 4.6 Decorator (guards de ruta)

`AuthenticationGuard(verifier)` ofrece dos decoradores:

- `require_authentication`: exige token válido.
- `require_role(*roles)`: exige token válido **y** uno de los roles.

**Qué resuelve:** repetir la verificación de token en cada ruta.
**Por qué:** es un aspecto transversal (*cross-cutting concern*); un decorador lo aplica de forma declarativa y uniforme.

Reglas a recordar:

- `require_role` ya autentica; **no** apilar ambos.
- `@app.route` debe ser el decorador **más externo**.
- El payload del token se guarda en `g.current_user` (es el payload, no un `User` de BD).

### 4.7 Factory (`uow_factory`, `create_session_factory`)

Los servicios reciben una *fábrica* de `UnitOfWork`, no una instancia.

**Qué resuelve:** que cada operación tenga su propia sesión/transacción.
**Por qué:** una sesión compartida entre peticiones concurrentes sería insegura y mezclaría transacciones.

### 4.8 Centralized error handling

Excepciones de dominio en `exceptions.py` (todas heredan de `AppError`) y `routes/error_handlers.py` las traduce a JSON/HTTP.

| Excepción | HTTP | Cuándo |
|---|---|---|
| `AuthenticationError` (`InvalidCredentialsError`, `InvalidTokenError`) | 401 | Credenciales o token malos |
| `AuthorizationError` | 403 | Token válido, rol insuficiente |
| `NotFoundError` | 404 | Recurso inexistente |

**Qué resuelve:** evitar `try/except` por todas partes y mensajes inconsistentes.
**Por qué:** los servicios hablan en términos de dominio, no de HTTP; un solo lugar decide el código de estado. Los mensajes son **genéricos a propósito** para no filtrar información (no revelar si un usuario existe).

### 4.9 Enum como fuente única de verdad

`Role` y `TokenType` son `StrEnum`.

**Qué resuelve:** errores por strings escritos a mano (`"admn"`).
**Por qué:** un solo lugar define los valores; el IDE y el análisis estático detectan errores, y como son `str` se guardan/serializan sin fricción.

---

## 5. Autenticación con JWT (RS256)

### 5.1 ¿Qué es un JWT?

Un token con tres partes `header.payload.signature`. El payload lleva *claims* (datos). La firma garantiza que no fue alterado. **No está cifrado**: no pongas secretos en él.

### 5.2 ¿Por qué RS256 (asimétrico) y no HS256?

| | HS256 | RS256 |
|---|---|---|
| Clave | Una secreta compartida | Par privada/pública |
| Quién firma | Quien tenga el secreto | Solo quien tiene la privada |
| Quién verifica | Quien tenga el secreto (y por tanto también podría firmar) | Cualquiera con la pública |

Con RS256, un servicio que solo verifica no puede falsificar tokens. Es la base de que `JwtVerifier` **nunca** reciba la clave privada. Las claves (RSA 3072, generadas con `openssl`) viven en `infrastructure/keys/`, están en `.gitignore` y se leen vía rutas del `.env`.

### 5.3 Claims y validaciones

`JwtSigner.encode(payload)` añade:

| Claim | Significado |
|---|---|
| `type` | `access` o `refresh` |
| `jti` | ID único del token (uuid4) |
| `iss` | Emisor |
| `aud` | Audiencia destinataria |
| `iat` | Momento de emisión |
| `exp` | Expiración |
| `sub` | Dueño del token (id de usuario como `str`; PyJWT lo exige) |

`JwtVerifier.decode(token)`:

- Fija `algorithms=["RS256"]` (evita el ataque de *algorithm confusion*, p. ej. `alg: none`).
- **Exige** `exp, iat, iss, aud, sub, type, jti`.
- Comprueba `type == expected_type`, así un refresh token **no sirve** como access token y viceversa.
- Ante cualquier fallo lanza `InvalidTokenError`.

### 5.4 Hash de contraseñas

`WerkzeugPasswordHasher` usa scrypt con sal. Las contraseñas **nunca** se guardan en claro.

Como un hash con sal es distinto cada vez, **no se puede buscar un usuario por hash**. Por eso el login hace: buscar por `username` → `verify(password, hash)` en el servicio.

### 5.5 Flujo de login

```
POST /login {username, password}
  → get_by_username  (NotFoundError → InvalidCredentialsError)
  → hasher.verify    (falla → InvalidCredentialsError)
  → emite access token (sub, role) + refresh token (sub)
  → guarda el jti del refresh token en BD
  ← TokenDTO {access_token, refresh_token, token_type}
```

Usuario inexistente y contraseña errónea devuelven **el mismo error** para evitar *user enumeration*.

---

## 6. Autorización por roles

- `User.role`: `String(20)`, `nullable=False`, `default=Role.USER.value`.
- El access token incluye `role`; el guard lo lee del token, **sin consultar la BD** en cada petición (rápido).
- `@guard.require_role(Role.ADMIN)` protege rutas de administrador.

Compromiso a conocer: como el rol viaja en el token, un cambio de rol no se aplica hasta que el access token expire (15 min por defecto, `ACCESS_TOKEN_EXPIRES_MINUTES`). Por eso el access token es de vida corta.

---

## 7. Refresh tokens con rotación

### 7.1 Por qué dos tokens

| Token | Vida | Uso | Riesgo si se roba |
|---|---|---|---|
| Access | Corta (15 min) | Se envía en cada petición | Limitado por su corta vida |
| Refresh | Larga (7 días) | Solo para obtener un par nuevo | Alto → se controla y rota |

Permite sesiones largas sin dejar un token poderoso viajando constantemente.

### 7.2 Qué se guarda en BD

Tabla `refresh_token`: `id`, `jti` (único), `user_id` (FK, indexado), `expires_at` (con zona horaria), `revoked`. **Solo el `jti`, nunca el token completo**: si la BD se filtra, no hay tokens utilizables. Esto da **revocabilidad** a un sistema de tokens que de otro modo sería sin estado.

### 7.3 Rotación y detección de reutilización

```
POST /refresh {refresh_token}
  → decodifica (type=refresh)
  → busca el jti en BD
       ├─ no existe / usuario no existe  → InvalidTokenError
       ├─ ya revocado (reutilización → posible robo)
       │     → revoca TODOS los tokens del usuario
       │     → commit ANTES de lanzar
       │     → InvalidTokenError
       └─ válido → lo revoca y emite un par nuevo
```

**Qué resuelve:** si alguien roba un refresh token y lo usa, cuando el dueño legítimo intente usar el suyo (ya revocado) o viceversa, el sistema detecta la reutilización y cierra todas las sesiones.
**Por qué:** un refresh token de un solo uso limita la ventana de ataque.

### 7.4 Logout

Revoca el refresh token recibido. Si el `jti` no existe es un **no-op silencioso** (idempotente) y devuelve 204: repetir el logout no da error y no revela información.

---

## 8. Facturación

### 8.1 Modelo de datos

```
User 1 ──── N Invoice 1 ──── N InvoiceDetail N ──── 1 Product
```

- `Invoice.user_id` (FK); `Invoice.user` ↔ `User.invoices`.
- `InvoiceDetail.invoice_id` (FK); `Invoice.invoice_details` ↔ `InvoiceDetail.invoice`.
- `InvoiceDetail.product` es **unidireccional** (`Product` no conoce los detalles): no hace falta y reduce acoplamiento.
- Dinero con `Numeric(12, 2)` / `Decimal` (los `float` introducen errores de redondeo).
- `InvoiceDetail.price` es un **snapshot** del precio del producto al momento de la venta: si el producto cambia de precio mañana, las facturas históricas no cambian.

### 8.2 Reglas de negocio (`InvoiceService.create`)

1. Para cada línea, `uow.products.get_by_id(product_id)`.
2. `price = Decimal(str(product.price))` (`Product.price` es `float`; pasar por `str` evita arrastrar imprecisión binaria).
3. `amount = price * quantity`.
4. `total_amount = suma de amounts`.
5. Crear factura + detalles en **una transacción**.

El cliente solo envía `product_id` y `quantity`. Todo importe lo calcula el servidor.

### 8.3 Acceso por propietario

- `GET /api/v1/invoices`: admin → todas; user → solo las suyas.
- `GET /api/v1/invoices/<id>`: admin → cualquiera; user → solo propia.
- `POST /api/v1/invoices`: cualquier autenticado; `user_id = int(g.current_user["sub"])`.
- Si un usuario pide una factura ajena, se lanza **`NotFoundError` (404), no 403**: así no se revela que esa factura existe.
- El **servicio no conoce roles**: recibe `user_id` (filtrar por dueño) o `None` (sin filtro). La **ruta** decide según el rol. Mantiene el servicio limpio y reutilizable.
- Las facturas son **inmutables a propósito** (sin PUT/DELETE), como en la práctica contable real.

---

## 9. Modelos y SQLAlchemy: puntos sutiles

- Todos los modelos heredan de `Base` (`infrastructure/db.py`).
- Cada modelo debe importarse en `models/__init__.py`; `create_schema` hace `import models`. Si falta, la tabla no se crea y las relaciones por string no resuelven.
- Las relaciones usan strings (`Mapped["Invoice"]`) para evitar importaciones circulares. Para silenciar a Pylance se importa la clase solo bajo `if TYPE_CHECKING:`, **nunca** un import real entre modelos.
- `create_schema` no altera tablas existentes: tras cambiar un modelo hay que recrear la tabla.

---

## 10. Configuración y secretos

- `.env` define `DATABASE_URL`, `JWT_PRIVATE_KEY_PATH`, `JWT_PUBLIC_KEY_PATH`; opcionales `ACCESS_TOKEN_EXPIRES_MINUTES` (15) y `REFRESH_TOKEN_EXPIRES_DAYS` (7).
- `get_int_env` valida que sean enteros positivos (`ConfigurationError` si no).
- Las claves y el `.env` **no se versionan**.
- Las claves se pasan a los adaptadores como **contenido (`str`)**, no como ruta: los adaptadores no tocan el disco, solo `app.py` (composition root) lee archivos.

---

## 11. Resumen: patrón → problema → motivo

| Patrón / práctica | Problema que resuelve | Por qué se eligió |
|---|---|---|
| Capas | Código mezclado y difícil de cambiar | Cada capa cambia por una razón |
| Hexagonal (puertos/adaptadores) | Dependencia de librerías externas | Cambiar PyJWT/werkzeug sin tocar negocio |
| Inyección de dependencias | Acoplamiento y poca testabilidad | Dependencias explícitas e intercambiables |
| Composition Root | Dependencias creadas en cualquier lugar | Un único sitio las ensambla |
| Repository | SQL/ORM disperso en servicios | Encapsula acceso a datos |
| Unit of Work | Operaciones parciales | Atomicidad de transacciones |
| DTO | Mass assignment y fuga de datos | Frontera controlada de la API |
| Decorator (guards) | Verificación repetida en rutas | Aspecto transversal declarativo |
| Manejo centralizado de errores | `try/except` y respuestas inconsistentes | Un único mapeo dominio → HTTP |
| Enum (`Role`, `TokenType`) | Strings mágicos | Fuente única de verdad |
| RS256 | Cualquier verificador podría falsificar | Solo la clave privada firma |
| Refresh con rotación | Robo de tokens de larga vida | Un solo uso + detección de reutilización |
| Snapshot de precio | Facturas históricas cambiantes | Integridad contable |
| 404 en lugar de 403 | Revelar existencia de recursos | Menor fuga de información |

---

## 12. Puntos abiertos (pendientes conocidos)

- **Primer admin**: los usuarios nuevos reciben `user`. Opciones: hacer público `POST /users` (seguro, el rol se asigna en servidor) y promover manualmente con `UPDATE "user" SET role = 'admin' WHERE username = '...'` (comillas en `"user"`, palabra reservada en PostgreSQL), o sembrar un admin. Tras promover, volver a iniciar sesión.
- **`PUT /users/<id>`** solo exige autenticación: cualquier usuario podría cambiar la contraseña de otro. Debería limitarse al propietario (`g.current_user["sub"]`) o a un admin.
- Usuarios creados antes de activar el hash tienen contraseña en texto plano y no pueden iniciar sesión: hay que recrearlos.
- Las funcionalidades de facturación y refresh tokens aún no se han probado de punta a punta.
- No hay suite de tests ni configuración de lint todavía.

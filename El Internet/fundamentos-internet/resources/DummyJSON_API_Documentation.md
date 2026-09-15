NOTA: Esta información fue generada con IA a partir de la colección que se proporcionó.

# Documentación API — DummyJSON (Productos)

Base URL: `https://dummyjson.com`

Colección con 12 operaciones sobre el recurso `products`. Cada una incluye un ejemplo de uso exitoso y un ejemplo de error o resultado vacío.

> **Nota:** las operaciones de escritura (`POST`, `PUT`, `PATCH`, `DELETE`) no persisten los cambios en el servidor; DummyJSON simula la respuesta pero no modifica los datos reales.

---

## 1. Obtener Productos

Lista todos los productos disponibles, paginados por defecto.

- **Método:** `GET`
- **URL:** `/products`

### Parámetros de URL
Ninguno.

### Query Parameters
Ninguno en el ejemplo (ver "Obtener Productos con Paginación" para `limit`/`skip`).

### Body
No aplica.

### Respuesta exitosa — `200 OK`
```json
{
  "products": [
    {
      "id": 1,
      "title": "Essence Mascara Lash Princess",
      "description": "The Essence Mascara Lash Princess is a popular mascara...",
      "category": "beauty",
      "price": 9.99,
      "discountPercentage": 10.48,
      "rating": 2.56,
      "stock": 99,
      "tags": ["beauty", "mascara"],
      "brand": "Essence"
    }
  ]
}
```

### Respuesta de error — `404 Not Found`
Ejemplo con endpoint mal escrito (`/producto` en vez de `/products`):
```html
<!DOCTYPE html>
<html lang="en">
  <title>Page not found — DummyJSON</title>
  ...
</html>
```

---

## 2. Obtener Producto

Obtiene el detalle de un producto por su ID.

- **Método:** `GET`
- **URL:** `/products/{id}`

### Parámetros de URL
| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | integer | Identificador único del producto |

### Query Parameters
Ninguno.

### Body
No aplica.

### Respuesta exitosa — `200 OK`
```json
{
  "id": 1,
  "title": "Essence Mascara Lash Princess",
  "description": "The Essence Mascara Lash Princess is a popular mascara...",
  "category": "beauty",
  "price": 9.99,
  "discountPercentage": 10.48,
  "rating": 2.56,
  "stock": 99,
  "tags": ["beauty", "mascara"],
  "brand": "Essence",
  "sku": "BEA-ESS-ESS-001",
  "weight": 4,
  "dimensions": { "width": "..." }
}
```

### Respuesta de error — `404 Not Found`
Ejemplo con `id=A` (no numérico / inexistente):
```json
{
  "message": "Product with id 'A' not found"
}
```

---

## 3. Obtener Productos por Categoría

Lista los productos pertenecientes a una categoría específica.

- **Método:** `GET`
- **URL:** `/products/category/{category}`

### Parámetros de URL
| Parámetro | Tipo | Descripción |
|---|---|---|
| `category` | string | Slug de la categoría (ej. `smartphones`) |

### Query Parameters
Ninguno.

### Body
No aplica.

### Respuesta exitosa — `200 OK`
```json
{
  "products": [
    {
      "id": 121,
      "title": "iPhone 5s",
      "description": "The iPhone 5s is a classic smartphone...",
      "category": "smartphones",
      "price": 199.99,
      "discountPercentage": 12.91,
      "rating": 2.83,
      "stock": 25,
      "tags": ["smartphones", "apple"],
      "brand": "Apple"
    }
  ]
}
```

### Respuesta "vacía" — `200 OK`
Ejemplo con categoría inexistente (`category=A`). No devuelve error, sino una lista vacía:
```json
{
  "products": [],
  "total": 0,
  "skip": 0,
  "limit": 0
}
```

---

## 4. Ordenar Productos

Lista productos aplicando un criterio de ordenamiento.

- **Método:** `GET`
- **URL:** `/products`

### Parámetros de URL
Ninguno.

### Query Parameters
| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `sortBy` | string | No | Campo por el cual ordenar (ej. `title`) |
| `order` | string | No | Dirección del orden: `asc` o `desc` |

### Body
No aplica.

### Respuesta exitosa — `200 OK`
Ejemplo: `?sortBy=title&order=asc`
```json
{
  "products": [
    {
      "id": 167,
      "title": "300 Touring",
      "description": "The 300 Touring is a stylish and comfortable sedan...",
      "category": "vehicle",
      "price": 28999.99,
      "discountPercentage": 3.98,
      "rating": 4.05,
      "stock": 54,
      "tags": ["sedans", "vehicles"],
      "brand": "Chrysler",
      "sku": "VEH-CHR-TOU-167",
      "weight": 9
    }
  ]
}
```

### Respuesta de error — `400 Bad Request`
Ejemplo con `order` inválido: `?sortBy=123&order=123`
```json
{
  "message": "Invalid 'order' - should be either 'asc' or 'desc'"
}
```

---

## 5. Buscar Productos

Busca productos cuyo contenido coincide con un texto.

- **Método:** `GET`
- **URL:** `/products/search`

### Parámetros de URL
Ninguno.

### Query Parameters
| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `q` | string | Sí | Texto de búsqueda |

### Body
No aplica.

### Respuesta exitosa — `200 OK`
Ejemplo: `?q=phone`
```json
{
  "products": [
    {
      "id": 101,
      "title": "Apple AirPods Max Silver",
      "description": "The Apple AirPods Max in Silver are premium over-ear headphones...",
      "category": "mobile-accessories",
      "price": 549.99,
      "discountPercentage": 13.67,
      "rating": 3.47,
      "stock": 59,
      "tags": ["electronics", "over-ear headphones"]
    }
  ]
}
```

### Respuesta de error
No se incluyó un caso de error específico para esta operación en la colección (una búsqueda sin resultados devolvería `200 OK` con `products: []`, de forma similar a los demás filtros).

---

## 6. Obtener Productos con Paginación

Lista productos controlando el tamaño de página y el desplazamiento.

- **Método:** `GET`
- **URL:** `/products`

### Parámetros de URL
Ninguno.

### Query Parameters
| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `limit` | integer | No | Cantidad máxima de resultados a devolver |
| `skip` | integer | No | Cantidad de resultados a omitir desde el inicio |

### Body
No aplica.

### Respuesta exitosa — `200 OK`
Ejemplo: `?limit=10&skip=10`
```json
{
  "products": [
    {
      "id": 11,
      "title": "Annibale Colombo Bed",
      "description": "The Annibale Colombo Bed is a luxurious and elegant bed frame...",
      "category": "furniture",
      "price": 1899.99,
      "discountPercentage": 8.57,
      "rating": 4.77,
      "stock": 88,
      "tags": ["furniture", "beds"],
      "brand": "Annibale Colombo",
      "sku": "FUR-ANN-ANN-011"
    }
  ]
}
```

### Respuesta "vacía" — `200 OK`
Ejemplo con `skip` mayor al total disponible: `?limit=10&skip=200`. No devuelve error, sino un array vacío:
```json
{
  "products": [],
  "total": 194,
  "skip": 200,
  "limit": 0
}
```

---

## 7. Obtener Campos Específicos de Productos

Lista productos devolviendo solo los campos indicados.

- **Método:** `GET`
- **URL:** `/products`

### Parámetros de URL
Ninguno.

### Query Parameters
| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `select` | string | No | Lista de campos separados por coma a incluir en la respuesta |

### Body
No aplica.

### Respuesta exitosa — `200 OK`
Ejemplo: `?select=title,price`
```json
{
  "products": [
    { "id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99 },
    { "id": 2, "title": "Eyeshadow Palette with Mirror", "price": 19.99 },
    { "id": 3, "title": "Powder Canister", "price": 14.99 }
  ]
}
```

### Respuesta con campos inválidos — `200 OK`
Ejemplo con campos inexistentes: `?select=A,B`. La API ignora los campos no reconocidos y devuelve solo `id`:
```json
{
  "products": [
    { "id": 1 },
    { "id": 2 },
    { "id": 3 }
  ]
}
```

---

## 8. Filtrar Productos por Fecha de Modificación

Lista productos cuya fecha de última modificación es posterior a la indicada.

- **Método:** `GET`
- **URL:** `/products`

### Parámetros de URL
Ninguno.

### Query Parameters
| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `modifiedAfter` | string (ISO 8601) | No | Fecha/hora mínima de última modificación |
| `select` | string | No | Campos a incluir en la respuesta |

### Body
No aplica.

### Respuesta exitosa — `200 OK`
Ejemplo: `?modifiedAfter=2026-06-01T00:00:00Z&select=title,meta`
```json
{
  "products": [
    {
      "id": 10,
      "title": "Gucci Bloom Eau de",
      "meta": {
        "createdAt": "2026-07-19T20:10:42.419Z",
        "updatedAt": "2026-07-27T15:21:17.071Z",
        "barcode": "3170832177880",
        "qrCode": "https://cdn.dummyjson.com/public/qr-code.png"
      }
    }
  ]
}
```

### Respuesta "vacía" — `200 OK`
Ejemplo con fecha futura sin coincidencias: `?modifiedAfter=2027-06-01T00:00:00Z&select=title,meta`
```json
{
  "products": [],
  "total": 0,
  "skip": 0,
  "limit": 0
}
```

---

## 9. Agregar Producto (No persiste)

Simula la creación de un nuevo producto.

- **Método:** `POST`
- **URL:** `/products/add`

### Parámetros de URL
Ninguno.

### Query Parameters
Ninguno.

### Body
`raw` / `application/json`. Acepta cualquier subconjunto de campos del modelo de producto.
```json
{
  "title": "Producto de Prueba"
}
```

### Respuesta exitosa — `201 Created`
DummyJSON asigna un nuevo `id` incremental y devuelve únicamente los campos enviados:
```json
{
  "id": 195,
  "title": "Producto de Prueba"
}
```

### Respuesta de error
No se incluyó un caso de error específico para esta operación en la colección.

---

## 10. Actualización de Producto — PUT (No persiste)

Simula el reemplazo completo de un producto existente.

- **Método:** `PUT`
- **URL:** `/products/{id}`

### Parámetros de URL
| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | integer | Identificador del producto a actualizar |

### Query Parameters
Ninguno.

### Body
`raw` / `application/json`.
```json
{
  "title": "Prueba Actualizar Producto"
}
```

### Respuesta exitosa — `200 OK`
Devuelve el producto original combinado con los campos enviados:
```json
{
  "id": 1,
  "title": "Prueba Actualizar Producto",
  "price": 9.99,
  "discountPercentage": 10.48,
  "stock": 99,
  "rating": 2.56,
  "images": ["https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"],
  "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp",
  "description": "The Essence Mascara Lash Princess is a popular mascara...",
  "brand": "Essence",
  "category": "beauty"
}
```

### Respuesta de error — `404 Not Found`
Ejemplo con `id=A` (no numérico / inexistente):
```json
{
  "message": "Product with id 'A' not found"
}
```

---

## 11. Actualización Parcial de Producto — PATCH (No persiste)

Simula la actualización parcial de un producto existente.

- **Método:** `PATCH`
- **URL:** `/products/{id}`

### Parámetros de URL
| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | integer | Identificador del producto a actualizar |

### Query Parameters
Ninguno.

### Body
`raw` / `application/json`. Solo se envían los campos a modificar.
```json
{
  "title": "Prueba Actualizar Producto"
}
```

### Respuesta exitosa — `200 OK`
Igual comportamiento que `PUT`: devuelve el producto original con los campos actualizados:
```json
{
  "id": 1,
  "title": "Prueba Actualizar Producto",
  "price": 9.99,
  "discountPercentage": 10.48,
  "stock": 99,
  "rating": 2.56,
  "images": ["https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"],
  "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp",
  "description": "The Essence Mascara Lash Princess is a popular mascara...",
  "brand": "Essence",
  "category": "beauty"
}
```

### Respuesta de error — `404 Not Found`
Ejemplo con `id=A` (no numérico / inexistente):
```json
{
  "message": "Product with id 'A' not found"
}
```

---

## 12. Eliminar Producto (No persiste)

Simula la eliminación de un producto.

- **Método:** `DELETE`
- **URL:** `/products/{id}`

### Parámetros de URL
| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | integer | Identificador del producto a eliminar |

### Query Parameters
Ninguno.

### Body
No aplica.

### Respuesta exitosa — `200 OK`
Devuelve el producto eliminado con los campos adicionales `isDeleted` y `deletedOn`:
```json
{
  "id": 1,
  "title": "Essence Mascara Lash Princess",
  "description": "The Essence Mascara Lash Princess is a popular mascara...",
  "category": "beauty",
  "price": 9.99,
  "discountPercentage": 10.48,
  "rating": 2.56,
  "stock": 99,
  "tags": ["beauty", "mascara"],
  "brand": "Essence",
  "sku": "BEA-ESS-ESS-001",
  "weight": 4,
  "isDeleted": true,
  "deletedOn": "2026-09-13T00:00:00.000Z"
}
```

### Respuesta de error — `404 Not Found`
Ejemplo con `id=A` (no numérico / inexistente):
```json
{
  "message": "Product with id 'A' not found"
}
```

---

## Resumen de endpoints

| # | Operación | Método | Endpoint |
|---|---|---|---|
| 1 | Obtener Productos | GET | `/products` |
| 2 | Obtener Producto | GET | `/products/{id}` |
| 3 | Obtener Productos por Categoría | GET | `/products/category/{category}` |
| 4 | Ordenar Productos | GET | `/products?sortBy&order` |
| 5 | Buscar Productos | GET | `/products/search?q` |
| 6 | Paginación | GET | `/products?limit&skip` |
| 7 | Campos específicos | GET | `/products?select` |
| 8 | Filtrar por fecha de modificación | GET | `/products?modifiedAfter` |
| 9 | Agregar Producto | POST | `/products/add` |
| 10 | Actualizar Producto (completo) | PUT | `/products/{id}` |
| 11 | Actualizar Producto (parcial) | PATCH | `/products/{id}` |
| 12 | Eliminar Producto | DELETE | `/products/{id}` |


Normalice las siguiente tablas:
Asegúrese de incluir en la solución todos los pasos y justificaciones sobre la normalización. También incluya todas las tablas intermedias por las que fue pasando antes de llegar a la solución final.

# Tabla Original
| Order ID | Customer Name | Customer Phone | Address | Item ID | Item Name | Price | Quantity | Special Request | Delivery Time |
|-|-|-|-|-|-|-|-|-|-|
| 001 | Alice | 123-456-7890 | 123 Main St | 101 | Cheeseburger | $8 | 2 | No onions | 6:00 PM |
| 001 | Alice | 123-456-7890 | 123 Main St | 102 | Fries | $3 | 1 | Extra ketchup | 6:00 PM |
| 002 | Bob | 987-654-3210 | 456 Elm St | 103 | Pizza | $12 | 1 | Extra cheese | 7:30 PM |
| 002 | Bob | 987-654-3210 | 4th Avenue | 102 | Fries | $3 | 2 | None | 7:30 PM |
| 003 | Claire | 555-123-4567 | 789 Oak St | 105 | Salad | $6 | 1 | No croutons | 12:00 PM |
| 004 | Claire | 555-123-4567 | 464 Georgia St | 106 | Water | $1 | 1 | None | 5:00 PM |

# Tablas Normalizadas

#### Table Customer
| Id | CustomerName | CustomerPhone | Address |
|-|-|-|-|
| 1 | Alice | 123-456-7890 | 123 Main St |
| 2 | Bob | 987-654-3210 | 456 Elm St |
| 3 | Claire | 555-123-4567 | 789 Oak St |

#### Table Product
| Id | Name | Price |
|-|-|-|
| P101 | Cheeseburger | $8 |
| P102 | Fries | $3 |
| P103 | Pizza | $12 |
| P105 | Salad | $6 |
| P106 | Water | $1 |

#### SpecialRequests
| Id | Name |
|-|-|
| 1 | No onions |
| 2 | Extra ketchup |
| 3 | Extra cheese |
| 4 | No croutons |

#### Table ProductSpecialRequests
| Id | ProductId | SpecialRequestId |
|-|-|-|
| 1 | P101 | 1 |
| 2 | P102 | 2 |
| 3 | P103 | 3 |
| 4 | P104 | 4 |

#### Table Order
| Id | Number | CustomerId | DeliveryTime |
|-|-|-|-|
| 1 | 001 | 1 | 6:00 PM |
| 2 | 002 | 2 | 7:30 PM |
| 3 | 003 | 3 | 12:00 PM |

#### Table OrderProducts
| Id | OrderId | ProductId | Quantity |
|-|-|-|-|
| 1 | 1 | P101 | 2 |
| 2 | 1 | P102 | 1 |
| 3 | 2 | P103 | 1 |
| 4 | 2 | P102 | 2 |
| 5 | 3 | P105 | 1 |
| 6 | 3 | P106 | 1 |

#### Table OrderProductsSpecialRequests
| Id | OrderProductId | ProductSpecialRequestId |
|-|-|-|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 5 | 4 |

## Explicación

La siguiente normalización se separa en dos tipos de tablas: catálogos y transaccionales.

* Las tablas de catálogos son aquellas que almacenan información reutilizable en muchas transacciones, por ejemplo, `Customer`. El registro de los clientes Alice, Bob y Claire se crean una sola vez y luego se acceden cada vez que solicitan una orden.

* Las tablas transaccionales son las que almacenan información cada vez que se realiza una transacción, valga la redundancia, en este caso, cada vez que se realiza una orden.

Esta clasificación es importante porque permite establecer cuáles atributos de la tabla origen pertenecen a un catálogo u cuáles a una transacción.

### Tablas Catálogo

Las columnas `CustomerName`, `CustomerPhone` y `Address` pertenecen al cliente, y como se repiten, solo se crean una vez en la tabla `Customer`.

Las columnas `ItemId`, `ItemPrice` y `Price`  pertenecen al Item o Producto, y como se repiten, solo se crean una vez en la tabla `Product`.

La columna `SpecialRequests` es un caso interesante. La interpretación que se realizó consiste en que los valores de dicha columna _no se repiten pero se identificó que están relacionados con los productos_, ya que, por ejemplo, no se puede solicitar un extra queso si el producto seleccionado es papas fritas. Entonces, se definió una tabla catálogo llamada `SpecialRequests` para almacenar los valores disponibles y una tabla llamada `ProductSpecialRequests`, donde se establecen cuales solicitudes especiales están disponibles para cada producto. Esta última tabla tiene una característica: a pesar de que tiene un `Id` como llave primaria, las columnas `ProductId` y `SpecialRequestId` **deben formar una llave única** para que la combinación de sus valores no se repita.

### Tablas Transaccionales

La tabla original es de `Orders`, por lo que claramente se identifica que las transacciones o movimientos están relacionados con órdenes.

Se identifican las columnas `OrderId`, `CustomerId` y `DeliveryTime` como campos de la tabla `Order`, donde `CustomerId` es una relación hacia la columna `Id` de la tabla `Customer`. Por medio de esta relación, se puede acceder al nombre, teléfono y dirección del cliente.

Se crea la tabla `OrderProducts` para almacenar todos los productos que fueron elegidos para cada orden. Aquí se usan las columnas `OrderId` y `ProductId` como relaciones hacia las tablas `Order`, `Product`, así como el campo `Quantity` para saber cuántas unidades del producto fueron ordenadas.

Por último, se crea una tabla `OrderProductsSpecialRequests` para almacenar los pedidos especiales que hizo el cliente para cada uno de los productos de su orden. Esta tabla tiene las columnas `ProductOrderId`, para saber a cuál registro de la orden y ahí se sabe cuál es el producto al que se le asignó la solicitud especial, y la columna `ProductSpecialRequestId` para indicar cuál es la solicitud especial.

## Cumplimiento de Formas de Normalización

### 1FN

Todas las tablas tienen llaves primarias y datos atómicos.

### 2FN

A pesar de que no se creó ninguna tabla con llaves compuestas, si se cumple con 2FN al cumplir con 1FN.

### 3FN

Todos los campos, especialmente nombres, fueron organizados de forma que pueden ser identificados por un Id.
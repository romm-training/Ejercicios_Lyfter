Normalice las siguiente tablas:
Asegúrese de incluir en la solución todos los pasos y justificaciones sobre la normalización. También incluya todas las tablas intermedias por las que fue pasando antes de llegar a la solución final.

# Tabla Original

| VIN |	Make | Model | Year | Color | Owner ID | Owner Name | Owner Phone | Insurance Company | Insurance Policy |
|-|-|-|-|-|-|-|-|-|-|
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 101 | Alice | 123-456-7890 | ABC Insurance | Fire & Theft |
| 1HGCM82633A |	Honda |	Accord | 2003 |	Silver | 102 | Bob | 987-654-3210 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL |	Honda |	CR-V | 2014 | Blue | 103 | Claire |	555-123-4567 | DEF Insurance | Collision |
| 1G1RA6EH1FU |	Chevrolet |	Volt | 2015 | Red |	104 | Dave | 111-222-3333 | GHI Insurance |	Basic Legal |

# Tablas Normalizadas

#### Tabla Make
| Id | Name |
|-|-|
| 1 | Honda |
| 2 | Chevrolet |

#### Tabla Year
| Id | Year |
|-|-|
| 1 | 2003 |
| 2 | 2014 |
| 3 | 2015 |

#### Tabla Color
| Id | Name |
|-|-|
| 1 | Silver |
| 2 | Blue |
| 3 | Red |

#### Table Owner
| Id | Code | Name | Phone |
|-|-|-|-|
| 1 | 101 | Alice | 123-456-7890 |
| 2 | 102 | Bob | 987-654-3210 |
| 3 | 103 | Claire | 555-123-4567 |
| 4 | 104 | Dave | 111-222-3333 |

#### Table InsuranceCompany
| Id | Name |
|-|-|
| 1 | ABC Insurance |
| 2 | XYZ Insurance |
| 3 | DEF Insurance |
| 4 | GHI Insurance |

#### InsurancePolicy
| Id | Name |
|-|-|
| 1 | Fire & Theft |
| 2 | Full Cover |
| 3 | Collision |
| 4 | Basic Legal |


#### Tabla Model
| Id | MakeId | Name | YearId | ColorId |
|-|-|-|-|-|
| 1 | 1 | Accord | 1 | 1 |
| 2 | 1 | CR-V | 2 | 2 |
| 3 | 2 | Volt | 3 | 3 |

#### Tabla InsuranceCompanyPolicy
| Id | InsuranceCompanyId | InsurancePolicyId |
|-|-|-|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |

#### Tabla Car
| Id | VIN | MakeId | ModelId | OwnerI |
|-|-|-|-|-|
| 1 | 1HGCM82633A | 1 | 1 | 1 |
| 2 | 1HGCM82633A | 1 | 1 | 2 |
| 3 | 5J6RM4H79EL | 1 | 2 | 3 |
| 4 | 1G1RA6EH1FU | 2 | 3 | 4 |

#### Tabla CarInsurance
| Id | CarId | InsuranceCompanyPolicyId |
|-|-|-|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |


## Explicación

La siguiente normalización se separa en dos tipos de tablas: catálogos simples y compuestos. Aquí no hay tablas transaccionales.

* Las tablas de catálogos simples son aquellas que almacenan información muy básica que son reutilizables en otros catálogos, por ejemplo, `Make`, `Year` y `Color`, las cuales se combinan para formar los modelos de carros.

* Las tablas de catálogos compuestos son las que almacenan información combinando varios catálogos simples, por ejemplo, `Model`.

### Tablas Catálogo Simples

Las tablas `Make`, `Year`, `Color`, `Owner`, `InsuranceCompany` e `InsurancePolicy` se consideran simples porque no tiene relación de dependencia con otras tablas.

### Tablas Catálogo Compuestos

Las tablas `Model`, `InsuranceCompanyPolicy`, `Car` y `CarInsurance` se consideran compuestas porque tienen una o varias relaciones de dependencia con otras tablas.

Las tablas `InsuranceCompanyPolicy` tiene como objetivo relacionar las compañías con las pólizas para luego asociarlas con los carros mediante un único campo.

En el caso de `CarInsurance`, lo que se pensó es que un carro podía tener más de una póliza de forma simultánea o histórica. Por ejemplo, podría ser que en 2003 tenía una póliza X con una compañía que ya no existe, entonces, se adquirió una póliza similar con otra compañía, pero se mantienen ambos registros como referencia histórica.

## Cumplimiento de Formas de Normalización

### 1FN

Todas las tablas tienen llaves primarias y datos atómicos.

### 2FN

A pesar de que no se creó ninguna tabla con llaves compuestas, si se cumple con 2FN al cumplir con 1FN.

### 3FN

Todos los campos, especialmente nombres, fueron organizados de forma que pueden ser identificados por un Id.
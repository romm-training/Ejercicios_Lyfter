💼 Proyecto: Gestor de Finanzas Personales (con FreeSimpleGUI)
🎯 Objetivo

. Desarrollar una aplicación con interfaz gráfica usando la biblioteca FreeSimpleGUI, que permita gestionar finanzas personales de forma sencilla. Este proyecto tiene como propósito poner en práctica todos los conceptos aprendidos durante el Módulo 1, especialmente:
    Modularización
    Manejo de archivos
    Validaciones
    Funciones
    Programación orientada a objetos (POO)
    Separación de lógica y presentación

✅ Requisitos técnicos

La aplicación debe:
OK. Mostrar una tabla de movimientos (gastos e ingresos).
OK. Incluir un botón para agregar una categoría:
   OK Al presionarlo, debe abrir una nueva ventana que permita ingresar una categoría (ej: Comida, Transporte, Entretenimiento...).
OK. Incluir un botón para agregar un gasto:
   OK Al presionarlo, debe abrir una nueva ventana que permita ingresar un título, monto y categoría del gasto.
OK. Incluir un botón para agregar un ingreso:
   OK Al presionarlo, debe abrir una nueva ventana que permita ingresar un título, monto y categoría del ingreso.
OK. Mostrar un mensaje de error si se intenta agregar un ingreso/gasto sin categorías disponibles.

💾 Persistencia de datos

. Al cerrar o hacer un cambio, el programa debe guardar automáticamente los datos en archivos.
OK. Al abrir el programa, debe cargar los datos previamente guardados (si existen).

🧠 Reglas de desarrollo

OK. Use clases para representar las entidades principales del sistema (Movimiento, Categoria, GestorFinanzas, etc.).
OK. Separe la lógica del programa en funciones pequeñas y reutilizables.
OK. Organice su código en módulos (interfaces.py, logica.py, persistencia.py, etc.).
OK. Use identificadores claros que indiquen el propósito de cada variable, función o clase.
OK. Aplique validaciones básicas en los formularios.
OK. Implemente pruebas unitarias simples.

🧪 Pruebas unitarias

OK. Se deben implementar mínimo 8 pruebas unitarias.
OK. Las funciones o clases a probar quedan a criterio del estudiante, pero se recomienda enfocarse en la lógica del programa y validaciones importantes.
OK. Las pruebas deben estar organizadas en un archivo aparte, por ejemplo: test_logica.py.

💡
OK   Recuerde que las pruebas deben poder ejecutarse de forma independiente, sin depender de la interfaz gráfica.

🔍 Proceso sugerido
OK. Hacer mockups de cada ventana.
OK. Investigar los elementos de FreeSimpleGUI necesarios.
OK. Diseñar la estructura de datos en memoria (clases y relaciones).
OK. Dividir el desarrollo en funciones/módulos probables por separado.
OK. Avanzar paso a paso: no seguir al siguiente módulo sin verificar que el anterior funciona correctamente.
OK. Documente dudas que le surjan durante el proceso.

Recomendaciones

OK. Investigue más sobre los elementos de FreeSimpleGUI en la documentación oficial.
OK. Lea todos los requerimientos y detalles técnicos cuidadosamente.
OK. Divida todos los requerimientos en tareas más pequeñas (dividir para conquistar).
OK. Haga notas de aquellos requerimientos que no sepa cómo desarrollar con exactitud.
OK. Divida la lógica del programa en funciones pequeñas y módulos.
OK. Escriba código limpio. Use identificadores específicos y fáciles de entender.
OK. Pregunte cualquier duda que tenga.

🔗 Recursos

. FreeSimpleGUI en PyPI
. Documentación oficial de PySimpleGUI

Requerimientos extra (opcionales)

OK  1. Filtrar movimientos (gastos e ingresos) por un rango de fechas definido por el usuario
    OK  Agregue dos campos (Fecha inicio y Fecha fin) en la ventana principal
    OK  Al presionar un botón como “Filtrar”, la tabla debe actualizarse mostrando solo los movimientos dentro de ese rango
    OK  Incluya validación del formato de fecha (dd/mm/yyyy)

Ejemplo:

Entrada:

[
    {"fecha": "02/07/2025", "título": "Salario", "monto": 1000, "tipo": "Ingreso"},
    {"fecha": "03/07/2025", "título": "Comida", "monto": -20, "tipo": "Gasto"},
    {"fecha": "12/07/2025", "título": "Ropa", "monto": -50, "tipo": "Gasto"}
]

Salida

Filtrando desde 01/07/2025 hasta 10/07/2025
Movimientos:
- 02/07/2025 | Salario | ₡1000
- 03/07/2025 | Comida | ₡-20

OK  2. Permitir al usuario definir la fecha del ingreso o gasto (en lugar de solo usar la actual)
    OK  Al agregar un nuevo gasto o ingreso, incluya un campo adicional para ingresar la fecha (por defecto puede ser hoy)
    FALTA Valide que la fecha sea válida y que no esté en el futuro

Ejemplo:

Entrada:

{
    "título": "Venta libro",
    "monto": 50,
    "tipo": "Ingreso",
    "fecha": "20/07/2025"
}

Salida correcta:

Nuevo ingreso agregado:
Fecha: 20/07/2025 | Título: Venta libro | Monto: ₡50 | Tipo: Ingreso

Salida si la fecha es incorrecta:

Error: Formato de fecha inválido (use dd/mm/yyyy)

Salida si la fecha es futura:

Error: La fecha no puede ser en el futuro

FALTA   3. Generar un archivo .csv con todos los movimientos y totales
    FALTA   Añada un botón “Exportar a CSV” en la ventana principal
    FALTA   Al presionarlo, cree un archivo con:
    FALTA   Encabezados: Fecha, Título, Monto, Categoría, Tipo
    FALTA   Suma total de ingresos, gastos, y balance neto al final

Ejemplo:

Entrada:

[
    {"fecha": "01/07/2025", "título": "Salario", "monto": 1200, "categoría": "Trabajo", "tipo": "Ingreso"},
    {"fecha": "02/07/2025", "título": "Comida", "monto": -100, "categoría": "Alimentación", "tipo": "Gasto"}
]

Salida en el CSV:

Fecha,Título,Monto,Categoría,Tipo
01/07/2025,Salario,1200,Trabajo,Ingreso
02/07/2025,Comida,-100,Alimentación,Gasto

Totales:
Ingresos: ₡1200
Gastos: ₡100
Balance Neto: ₡1100

FALTA   4. Asignar un color personalizado a cada categoría
    OK  Al crear o editar una categoría, permita seleccionar un color con sg.ColorChooserButton
FALTA   Al mostrar los movimientos en la tabla, use el color asociado a su categoría
    OK  Asegúrese de guardar esta información junto con las categorías

Ejemplo:

Entrada:

Categoría: "Comida"

Color elegido: "#FFA500" (naranja)

{"fecha": "03/07/2025", "título": "Pizza", "monto": -40, "categoría": "Comida", "tipo": "Gasto"}

Salida:

En la tabla del GUI, la fila de "Pizza" aparece con color de fondo #FFA500 (naranja)

A nivel de base de datos:

{
    "categorías": {
        "Comida": "#FFA500"
    }
}
employees = [
    {"name": "Carlos", "email": "carlos@empresa.com", "department": "Ventas"},
    {"name": "Ana", "email": "ana@empresa.com", "department": "TI"},
    {"name": "Luis", "email": "luis@empresa.com", "department": "Ventas"},
    {"name": "Sofía", "email": "sofia@empresa.com", "department": "RRHH"},
    {"name": "Mario", "email": "mario@empresa.com", "department": "RRHH"},
    {"name": "Luz", "email": "luz@empresa.com", "department": "Ventas"},
    {"name": "Maria", "email": "maria@empresa.com", "department": "Ventas"},
    {"name": "Jose", "email": "jose@empresa.com", "department": "Gerencia"},
    {"name": "Ever", "email": "ever@empresa.com", "department": "Mensajeria"},
    {"name": "Marcia", "email": "marcia@empresa.com", "department": "Mercadeo"},
    {"name": "Julio", "email": "julio@empresa.com", "department": "Ventas"},
]

departments = []
temp_department = ""
employee_name = ""
department_exists = False

#Recorre la lista de empleados
for employee in employees:
    temp_department = employee["department"]
    employee_name = employee["name"]

    #Si la lista de departamentos esta vacia, inserta el primer elemento. 
    #Si no, recorre para ver si ya existe el departamento.
    #Si ya existe el departamento, agrega el nombre del empleado a la lista.
    #Si no existe el departamento, lo crea y en la lista de empleados incluye el empleado actual del ciclo.
    if len(departments) == 0:
        departments.append({temp_department: [employee_name]})
    else:
        for department in departments:
            if department.get(temp_department) != None:
                department[temp_department].append(employee_name)
                department_exists = True
                break
                
        if not department_exists:
            departments.append({temp_department: [employee_name]})

    department_exists = False

print(departments)
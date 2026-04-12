list_of_keys = ["access_level", "age"]
employee = {
    "name": "John",
    "email": "john@ecorp.com",
    "access_level": 5,
    "age": 28
}

print(f"Diccionario antes: {employee}")

for key_to_delete in list_of_keys:
    for key in employee.keys():
        if key_to_delete == key:
            employee.pop(key_to_delete)
            break

print(f"Diccionario despues: {employee}")
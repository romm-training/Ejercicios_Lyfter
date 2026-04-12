def main():
    name = ""
    age = 0

    try:
        name = input("Ingrese su nombre: ")
        if name.isdigit():
            raise ValueError("El nombre no puede ser un numero")
    
        age = input("Ingrese su edad: ")

        if not age.isdigit():
            raise ValueError("Numero no valido")
        
        print(f"Hola {name}, su edad es {age}")
    except ValueError as ex:
        print(ex)

if __name__ == "__main__":
    main()
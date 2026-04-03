def print_menu():
    menu = """
    1. Suma
    2. Resta
    3. Multiplicación
    4. División
    5. Borrar Resultado
    """
    print(menu)

def addition(number1, number2):
    return number1 + number2

def substraction(number1, number2):
    return number1 - number2

def multiplication(number1, number2):
    return number1 * number2

def division(number1, number2):
    try:
        if number2 == 0:
            raise ZeroDivisionError()
        return number1 / number2
    except ZeroDivisionError:
        print("No se puede realizar división por 0. Intente de nuevo.")
        return number1

def calculator(number1, number2, operation):
    result = 0
    match operation:
        case 1:
            result = addition(number1, number2)
        case 2:
            result = substraction(number1, number2)
        case 3:
            result = multiplication(number1, number2)
        case 4:
            result = division(number1, number2)
        case 5:
            result = 0

    return result

def input_number():
    flow_control = 1
    number = 0

    while flow_control == 1:
        try:
            number = float(input("Ingrese el numero: "))
            flow_control = 0
        except ValueError:
            print("El número es incorrecto. Intente de nuevo.")
            continue
    
    return number

def input_operation():
    flow_control = 1
    operation = 1

    while flow_control == 1:
        try:
            operation = int(input("Ingrese la operación que desea realizar: "))
            
            if operation < 1 or operation > 5:
                raise ValueError()
            
            flow_control = 0
        except ValueError:
            print("La opción ingresada es incorrecta. Intente de nuevo.")
            continue

    return operation

def input_flow_control():
    local_flow_control = 1
    flow_control = 1
    while local_flow_control == 1:
        try:
            flow_control = int(input("Desea continuar? 1-SI 0-NO: "))
            if flow_control != 0 and flow_control != 1:
                raise ValueError()
            local_flow_control = 0
        except ValueError:
            print("La opción ingresada es incorrecta. El programa continua.")
            continue

    return flow_control


def main():
    flow_control = 1
    number1 = input_number()
    number2 = 0

    while flow_control == 1:
        try:
            print_menu()
            
            operation = input_operation()

            if operation >= 1 and operation <= 4:
                number2 = input_number()

            number1 = calculator(number1, number2, operation)
            
            print(f"Resultado: {number1}")

            flow_control = input_flow_control()
        except Exception as ex:
            print(f"Se ha presentado un error inesperado. El proceso continua. {ex}")
            flow_control = 1

if __name__ == "__main__":
    main()
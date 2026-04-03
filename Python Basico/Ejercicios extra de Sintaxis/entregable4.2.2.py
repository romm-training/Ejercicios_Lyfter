number1 = int(input("Ingrese el numero1: "))
number2 = int(input("Ingrese el numero2: "))
number3 = int(input("Ingrese el numero3: "))

right_message = "Correcto"
wrong_message = "Incorrecto"

if number1 == 30 or number2 == 30 or number3 == 30:
    message = right_message
else:
    total = number1 + number2 + number3
    if total == 30:
        message = right_message
    else:
        message = wrong_message

print(message)
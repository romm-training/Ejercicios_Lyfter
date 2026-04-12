number1 = int(input("Ingrese el numero1: "))
number2 = int(input("Ingrese el numero2: "))
number3 = int(input("Ingrese el numero3: "))

greater = 0

if (number2 > number1):
    if (number2 > number3):
        greater = number2
    else:
        greater = number3
elif (number1 > number3):
    greater = number1
else:
    greater = number3

print(f"El numero mayor es: {greater}")
import random

secret_number = random.randint(1,10)

flow_controller = True

while (flow_controller):
    number = int(input("Ingrese un numero entre 1 y 10: "))
    flow_controller = number != secret_number

print(f"Correcto! El numero secreto es {secret_number}")

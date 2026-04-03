my_list = []
input_number = 0
greater = 0

for index in range(0,10):
    input_number = int(input("Ingrese un numero: "))
    my_list.append(input_number)
    if input_number > greater:
        greater = input_number

print(f"La lista completa es: {my_list} y el numero mas alto es: {greater}")
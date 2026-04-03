input_list = input("Ingrese una lista de numeros separados por coma: ")
final_list = []

for number in input_list.split(','):
    final_list.append(int(number))

number_to_search = int(input("Ingrese el numero que desea buscar: "))

number_count = 0

for number in final_list:
    if number == number_to_search:
        number_count = number_count + 1

print(f"El numero {number_to_search} aparece {number_count} veces")


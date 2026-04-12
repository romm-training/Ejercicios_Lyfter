#my_list = [3,6,0,2,4]
#my_list = [3,6,0,-2,4]
my_list = [3,6,7,2,4]

result = "Todos los numeros son positivos"
for number in my_list:
    if number <= 0:
        result = "Hay al menos un numero negativo o cero"

print(result)
def quantity_of_char_in_string(str, chr):
    count = 0
    for c in str:
        if c == chr:
            count = count + 1

    return count

my_string = input("Ingrese una palabra o frase: ")
my_char = input("Ingrese el caracter que desea buscar: ")

quantity = quantity_of_char_in_string(my_string, my_char)

if quantity == 0:
    print(f"El caracter {my_char} no se ha encontrado.")
elif quantity == 1:
    print(f"El caracter {my_char} se ha encontrado {quantity} vez.")
else:
    print(f"El caracter {my_char} se ha encontrado {quantity} veces.")
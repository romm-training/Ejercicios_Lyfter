def number_of_vocals_in_string(str):
    vocal_list = ["a","e","i","o","u"]
    count = 0

    for c in str:
        if c in vocal_list:
            count = count + 1

    return count

my_string = "Hola mundooooo!!!"
print(f"Cantidad de vocales en '{my_string}': {number_of_vocals_in_string(my_string)}")
def sum_of_values(str_list):
    total = 0
    tmp_number = 0
    for str in str_list:
        try:
            tmp_number = float(str)
            total = total + tmp_number
            print(f"{str} sumado correctamente")
        except ValueError:
            print(f"Elemento inválido: {str}")

    print(f"El total es: {total}")

def main():
    my_list = ['10', 'manzana', '5.5', '3', 'n/a']
    sum_of_values(my_list)

if __name__ == "__main__":
    main()
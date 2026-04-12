def convert_to_integer(str_list):
    tmp_number = 0
    print("Resultado: ")
    for str in str_list:
        try:
            tmp_number = int(str)
            print(f"'{str}' convertido a {tmp_number}")
        except ValueError:
            print(f"No se logró convertir el elemento: {str}")

def main():
    my_list = ['4', 'hola', '10', '5.2']
    convert_to_integer(my_list)

if __name__ == "__main__":
    main()


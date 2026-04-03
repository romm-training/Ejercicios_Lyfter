import os

DEFAULT_ENCODING = "utf-8"

def append_string_to_file(file_path, str):
    with open(file_path, "a") as file:
        file.write(str)
    

def main():
    target_file_path = os.path.join(os.path.dirname(__file__),"Entregable14_4.txt")
    user_str = input("Ingrese un texto: ")
    user_str = user_str + "\n"
    append_string_to_file(target_file_path, user_str)
    print("El texto se agrega al final del archivo sin borrar lo anterior")

if __name__ == "__main__":
    main()
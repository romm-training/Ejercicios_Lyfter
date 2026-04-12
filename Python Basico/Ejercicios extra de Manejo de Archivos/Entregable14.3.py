import os

DEFAULT_ENCODING = "utf-8"

def read_file(file_path):
    file_list = []
    with open(file_path, encoding=DEFAULT_ENCODING) as file:
        file_list = file.readlines()

    return file_list

def write_file(file_path, file_list):
    with open(file_path, "w", encoding=DEFAULT_ENCODING) as file:
        file.writelines(file_list)

def convert_list_to_uppercase(source_list):
    #new_list = []
    #for element in source_list:
    #    new_list.append(element.upper())
    new_list = [word.upper() for word in source_list]
    return new_list

def main():
    file_path = os.path.join(os.path.dirname(__file__),"Entregable14_3.txt")
    target_file_path = os.path.join(os.path.dirname(__file__),"Entregable14_3_mayusculas.txt")
    file_content_list = read_file(file_path)
    write_file(target_file_path, convert_list_to_uppercase(file_content_list))


if __name__ == "__main__":
    main()
import os

DEFAULT_ENCODING = "utf-8"

def read_file(path_to_file):
    file_list = []
    with open(path_to_file, encoding=DEFAULT_ENCODING) as file:
        for line in file.readlines():
            file_list.append(line)
    
    return file_list

def write_to_file_without_line_breaks(target_file_path, file_list):
    str = " ".join(file_list).replace("\n","")
    with open(target_file_path, "w", encoding=DEFAULT_ENCODING) as file:
        file.write(str)

def main():
    file_path = os.path.join(os.path.dirname(__file__), "Entregable14_1.txt")
    target_file_name = os.path.join(os.path.dirname(__file__),"Entregable14_1_destino.txt")
    my_list = read_file(file_path)
    write_to_file_without_line_breaks(target_file_name, my_list)

if __name__ == "__main__":
    main()
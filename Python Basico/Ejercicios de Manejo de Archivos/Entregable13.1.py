import os

DEFAULT_ENCODING = "utf-8"

def read_file_into_list(path_to_file):
    file_elements = []
    with open(path_to_file,encoding=DEFAULT_ENCODING) as file:
        for line in file.readlines():
            file_elements.append(line)

    return file_elements

def write_list_into_file(path_to_file, file_elements):
    with open(path_to_file, "w",encoding=DEFAULT_ENCODING) as file:
        for element in file_elements:
            file.write(element)

def main():
    songs_file_name = os.path.join(os.path.dirname(__file__), "Entregable13_1_canciones.txt")
    target_file_name = os.path.join(os.path.dirname(__file__),"Entregable13_1_canciones_ordenadas.txt")
    file_elements_list = read_file_into_list(songs_file_name)
    file_elements_list.sort()
    write_list_into_file(target_file_name, file_elements_list)

if __name__ == "__main__":
    main()
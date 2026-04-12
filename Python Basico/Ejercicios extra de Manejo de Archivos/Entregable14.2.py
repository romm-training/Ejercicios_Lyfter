import os

DEFAULT_ENCODING = "utf-8"

def read_file_content(file_path):
    with open(file_path, encoding=DEFAULT_ENCODING) as file:
        return file.read()

def count_words(str):
    str = str.replace("\n"," ")
    word_list = str.split()
    return len(word_list)

def main():
    file_path = os.path.join(os.path.dirname(__file__),"Entregable14_2.txt")
    file_content = read_file_content(file_path)
    print(f"Este archivo contiene {count_words(file_content)} palabras")


if __name__ == "__main__":
    main()
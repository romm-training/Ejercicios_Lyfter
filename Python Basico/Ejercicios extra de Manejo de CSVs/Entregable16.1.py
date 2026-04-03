import os, csv

DEFAULT_ENCODING = "utf-8"

def print_csv_row(headers, row):
    print(f"Nombre: {row[0]}")
    print(f"Género: {row[1]}")
    print(f"Desarrollador: {row[2]}")
    print(f"Clasificación: {row[3]}")
    print("______________________________________")

def read_csv(file_path):
    row_count = 0
    headers = {}
    with open(file_path, "r", encoding=DEFAULT_ENCODING) as file:
        reader = csv.reader(file)
        for row in reader:
            if row_count == 0:
                headers = row
                row_count = row_count + 1
                continue
            print_csv_row(headers, row)



def main():
    file_path = os.path.join(os.path.dirname(__file__),"Videojuegos.csv")
    read_csv(file_path)


if __name__ == "__main__":
    main()
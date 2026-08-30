import csv, os

from dto import category_dto

_DEFAULT_ENCODING = "utf-8"
_DATA_FILE_NAME = "categories.csv"
_HEADERS = category_dto.Category_Dto.headers()

def _get_data_file_path():
    return os.path.join(os.path.dirname(__file__), _DATA_FILE_NAME)

def _get_if_file_exists(file_path):
    return os.path.exists(file_path)

def read_data():
    file_path = _get_data_file_path()

    if not _get_if_file_exists(file_path):
        raise FileNotFoundError("El archivo de datos no existe en la ruta indicada.")

    with open(file_path, "r", encoding=_DEFAULT_ENCODING) as file:
        data = []
        reader = csv.DictReader(file)
        data = [category_dto.Category_Dto(
            row["movement_type"],
            row["name"],
            row["color"]
        ) for row in reader]

        return data

def add_data(data: category_dto.Category_Dto):
    file_path = _get_data_file_path()

    file_exists = _get_if_file_exists(file_path)

    with open(file_path, "a", encoding=_DEFAULT_ENCODING, newline="") as file:
        writer = csv.DictWriter(file,fieldnames= _HEADERS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data.to_dict())

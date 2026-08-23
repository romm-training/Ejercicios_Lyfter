import csv, os

from dto import movement_dto

_DEFAULT_ENCODING = "utf-8"
_DATA_FILE_NAME = "movements.csv"
_HEADERS = movement_dto.Movement_Dto.headers()

def _get_data_file_path():
    return os.path.join(os.path.dirname(__file__), _DATA_FILE_NAME)

def _get_if_file_exists(file_path):
    if os.path.exists(file_path):
        return True
    return False

def read_data():
    file_path = _get_data_file_path()

    if not _get_if_file_exists(file_path):
        raise FileNotFoundError("El archivo de datos no existe en la ruta indicada.")

    with open(file_path, "r", encoding=_DEFAULT_ENCODING) as file:
        data = []
        reader = csv.DictReader(file)
        data = [movement_dto.Movement_Dto(
                row["date"],
                row["type"],
                row["category"],
                row["description"],
                row["amount"]
            ) for row in reader]

        return data

def write_data(data):
    file_path = _get_data_file_path()

    #if not _get_if_file_exists(file_path):
    #    raise FileNotFoundError("El archivo de datos no existe en la ruta indicada.")

    with open(file_path, "w", encoding=_DEFAULT_ENCODING, newline="") as file:
        writer = csv.DictWriter(file, _HEADERS)
        writer.writeheader()
        writer.writerows(data.to_dict())
        
def append_data(data):
    file_path = _get_data_file_path()

    file_exists = _get_if_file_exists(file_path)

    #if not _get_if_file_exists(file_path):
    #    raise FileNotFoundError("El archivo de datos no existe en la ruta indicada.")

    with open(file_path, "a", encoding=_DEFAULT_ENCODING, newline="") as file:
        writer = csv.DictWriter(file, _HEADERS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data.to_dict())

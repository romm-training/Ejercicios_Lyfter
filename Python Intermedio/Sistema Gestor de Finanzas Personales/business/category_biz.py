from dto import category_dto
from persistency import persistency_category

class _CONSTANTS():
    DATE_FORMAT = "%d/%m/%Y"
    COMBO_DEFAULT_VALUE = "--Seleccione--"
    AMOUNT_REGEX = r"^\d+(\.\d{1,2})?$"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")

class _FIELD_KEYS():
    CATEGORY_NAME = "category_name"
    CATEGORY_TYPE = "category_type"
    CATEGORY_COLOR = "category_color"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")


class Category_Biz():
    def add_data(self, category: category_dto):
        persistency_category.add_data(category)

    def read_data(self) -> list:
        data = []
        try:
            data = persistency_category.read_data()
        except FileNotFoundError as e:
            print(f"Error: {e}")
        return data

    # Lista la condicion y mensaje de las reglas de validacion y retorna las que se cumplen.
    def category_validations(self, values) -> list:
        rules = [
            (values[_FIELD_KEYS.CATEGORY_TYPE] == _CONSTANTS.COMBO_DEFAULT_VALUE, "Debe seleccionar el tipo de movimiento al que pertenece la categoría."),
            (not values[_FIELD_KEYS.CATEGORY_NAME].strip(), "Debe ingresar el nombre de la categoría."),
            (not values[_FIELD_KEYS.CATEGORY_COLOR].strip(), "Debe seleccionar un color.")
        ]

        return [message for condition, message in rules if condition]

      
from dto import movement_dto
from persistency import persistency_movement
from business import category_biz
from datetime import datetime
import re

class _CONSTANTS():
    DATE_FORMAT = "%d/%m/%Y"
    COMBO_DEFAULT_VALUE = "--Seleccione--"
    AMOUNT_REGEX = r"^-?\d+(\.\d{1,2})?$"
    TYPE_VALID_VALUES = ["Ingreso","Gasto"]

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")

class _FIELD_KEYS():
    MOVEMENT_DATE = "movement_date"
    MOVEMENT_DATE_CALENDAR = "movement_date_calendar"
    MOVEMENT_TYPE = "movement_type"
    MOVEMENT_DESCRIPTION = "movement_description"
    MOVEMENT_AMOUNT = "movement_amount"
    MOVEMENT_CATEGORY = "movement_category"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")

class Movement_Biz():
    def add_data(self, movement: movement_dto):
        persistency_movement.add_data(movement)

    def read_data(self) -> list:
        data = []
        try:
            data = persistency_movement.read_data()
        except FileNotFoundError as e:
            print(f"Error: {e}")
        return data

    # Usa expresion regular para validar si el monto es valido.
    def is_valid_amount(self, amount: float) -> bool:
        amount_pattern = re.compile(_CONSTANTS.AMOUNT_REGEX)
        return bool(amount_pattern.match(str(amount).strip()))

    # Lista la condicion y mensaje de las reglas de validacion y retorna las que se cumplen.
    def movement_validations(self, values, categories = []) -> list:
        if categories == []:
            categories = category_biz.Category_Biz().read_data()
        category_names = {c.name for c in categories}

        rules = [
            (
                not values[_FIELD_KEYS.MOVEMENT_DATE].strip(), 
                "Debe seleccionar una fecha de movimiento."
            ),
            (
                values[_FIELD_KEYS.MOVEMENT_DATE].strip() and datetime.strptime(values[_FIELD_KEYS.MOVEMENT_DATE].strip(), _CONSTANTS.DATE_FORMAT) > datetime.today(),
                "La fecha del movimiento no puede ser una fecha futura."
            ),
            (
                values[_FIELD_KEYS.MOVEMENT_TYPE] not in _CONSTANTS.TYPE_VALID_VALUES,
                "El tipo de movimiento es inválido."
            ),
            (
                values[_FIELD_KEYS.MOVEMENT_CATEGORY] == _CONSTANTS.COMBO_DEFAULT_VALUE,
                "Debe seleccionar una categoría."
            ),
            (
                values[_FIELD_KEYS.MOVEMENT_CATEGORY] not in category_names,
                "Debe seleccionar una categoría válida."
            ),
            (
                not values[_FIELD_KEYS.MOVEMENT_DESCRIPTION].strip(),
                "Debe ingresar una descripción."
            ),
            (
                not self.is_valid_amount(values[_FIELD_KEYS.MOVEMENT_AMOUNT]),
                "Debe ingresar un monto valido."
            )
        ]

        return [message for condition, message in rules if condition]

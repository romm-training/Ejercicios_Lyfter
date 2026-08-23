import FreeSimpleGUI as sg
from datetime import datetime

from dto import category_dto, movement_dto
from business import category_biz, movement_biz

class _CONSTANTS():
    DATE_FORMAT = "%d/%m/%Y"
    COMBO_DEFAULT_VALUE = "--Seleccione--"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")

class _KEYS():
    FROM_DATE = "from_date"
    FROM_DATE_CALENDAR = "from_date_calendar"
    TO_DATE = "to_date"
    TO_DATE_CALENDAR = "to_date_calendar"
    TBL_MOVEMENTS = "tbl_movements"
    MOVEMENT_DATE = "movement_date"
    MOVEMENT_DATE_CALENDAR = "movement_date_calendar"
    MOVEMENT_TYPE = "movement_type"
    MOVEMENT_DESCRIPTION = "movement_description"
    MOVEMENT_AMOUNT = "movement_amount"
    MOVEMENT_CATEGORY = "movement_category"
    CATEGORY_NAME = "category_name"
    CATEGORY_TYPE = "category_type"
    CATEGORY_COLOR = "category_color"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")

def movement_screen(movement_type):
    categories = category_biz.Category_Biz.read_data()

    filtered_categories = sorted([c.name for c in categories if c.movement_type == movement_type])

    cat_to_show = [_CONSTANTS.COMBO_DEFAULT_VALUE] + filtered_categories

    layout = [
        [sg.Text("Agregar un Movimiento")],
        [sg.Text("Tipo: "), sg.InputText(movement_type, key=_KEYS.MOVEMENT_TYPE, disabled=True)],
        [sg.Text(f"Fecha: "), sg.InputText("", key=_KEYS.MOVEMENT_DATE, size=(12,1), readonly=True, enable_events=True), sg.CalendarButton("📅", key=_KEYS.MOVEMENT_DATE_CALENDAR, target=_KEYS.MOVEMENT_DATE, format=_CONSTANTS.DATE_FORMAT, no_titlebar=False)],
        [sg.Text("Categoria: "), sg.Combo(values=cat_to_show, key=_KEYS.MOVEMENT_CATEGORY, default_value=_CONSTANTS.COMBO_DEFAULT_VALUE)],
        [sg.Text("Descripcion: "), sg.InputText(key=_KEYS.MOVEMENT_DESCRIPTION)],
        [sg.Text("Amount: "), sg.InputText(key=_KEYS.MOVEMENT_AMOUNT,size=(15,1))],
        [sg.Button("Guardar"),sg.Button("Cancelar")]
    ]

    window = sg.Window("Agregar Movimientos", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == _KEYS.MOVEMENT_DATE:
            try:
                date_from_input_text = datetime.strptime(values[_KEYS.MOVEMENT_DATE], _CONSTANTS.DATE_FORMAT)
                window[_KEYS.MOVEMENT_DATE_CALENDAR].calendar_default_date_M_D_Y = (
                date_from_input_text.month,
                date_from_input_text.day,
                date_from_input_text.year,
                )
            except ValueError:
                pass

        if event == "Guardar":
            movement = movement_dto.Movement_Dto(
                values[_KEYS.MOVEMENT_DATE], 
                values[_KEYS.MOVEMENT_TYPE],
                values[_KEYS.MOVEMENT_CATEGORY],
                values[_KEYS.MOVEMENT_DESCRIPTION],
                values[_KEYS.MOVEMENT_AMOUNT]
            )
            
            movement_biz.Movement_Biz.add_data(movement)
            
            window[_KEYS.MOVEMENT_DATE].update("")
            window[_KEYS.MOVEMENT_CATEGORY].update(_CONSTANTS.COMBO_DEFAULT_VALUE)
            window[_KEYS.MOVEMENT_AMOUNT].update("")
            window[_KEYS.MOVEMENT_DESCRIPTION].update("")

    window.close()

def category_screen():
    layout = [
            [sg.Text("Agregar una Categoria")],
            [sg.Text("Tipo: "), sg.Combo(values=[_CONSTANTS.COMBO_DEFAULT_VALUE, "Ingreso","Gasto"], key=_KEYS.CATEGORY_TYPE, default_value=_CONSTANTS.COMBO_DEFAULT_VALUE)],
            [sg.Text("Nombre: "), sg.InputText("", key=_KEYS.CATEGORY_NAME)],
            [sg.Text("Color: "), sg.Input(key=_KEYS.CATEGORY_COLOR, size=(10,1)), sg.ColorChooserButton("Elegir")],
            [sg.Button("Guardar"),sg.Button("Cancelar")]
        ]

    window = sg.Window("Ingresar Categorias", layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Guardar":
            category = category_dto.Category_Dto(
                values[_KEYS.CATEGORY_TYPE], 
                values[_KEYS.CATEGORY_NAME],
                values[_KEYS.CATEGORY_COLOR]
            )

            category_biz.Category_Biz.append_data(category)

        window[_KEYS.CATEGORY_TYPE].update(_CONSTANTS.COMBO_DEFAULT_VALUE)
        window[_KEYS.CATEGORY_NAME].update("")
        window[_KEYS.CATEGORY_COLOR].update("")

    window.close()

def load_table_data():
    movements_data = movement_biz.Movement_Biz.read_data()
    data_list = [[m.date, m.type, m.category, m.description, m.amount] for m in movements_data]
    return data_list

layout = [
    [sg.Text("Gestor de Finanzas Personales")],
    [sg.Text("Fecha Inicial: "), sg.InputText("", key=_KEYS.FROM_DATE, size=(11,1), enable_events=True, readonly=True), sg.CalendarButton("📅", key=_KEYS.FROM_DATE_CALENDAR, target=_KEYS.FROM_DATE, format=_CONSTANTS.DATE_FORMAT, no_titlebar=False, close_when_date_chosen=True), sg.Text("Fecha Final: "), sg.InputText("", key=_KEYS.TO_DATE, size=(11,1), enable_events=True, readonly=True), sg.CalendarButton("📅", key=_KEYS.TO_DATE_CALENDAR, target=_KEYS.TO_DATE, format=_CONSTANTS.DATE_FORMAT,no_titlebar=False, close_when_date_chosen=True), sg.Button("Filtrar")],
    [sg.Table(values=load_table_data(),headings=["Fecha","Tipo","Categoria","Descripcion","Monto"],auto_size_columns=True,key=_KEYS.TBL_MOVEMENTS, justification="center")],
    [sg.Button("Ingreso"), sg.Button("Gasto"), sg.Button("Categoria")],
]

window = sg.Window("Gestor de Finanzas Personales", layout)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == _KEYS.FROM_DATE:
        try:
            date_from_input_text = datetime.strptime(values[_KEYS.FROM_DATE], _CONSTANTS.DATE_FORMAT)
            window[_KEYS.FROM_DATE_CALENDAR].calendar_default_date_M_D_Y = (
            date_from_input_text.month,
            date_from_input_text.day,
            date_from_input_text.year,
            )
        except ValueError:
            pass

    if event == _KEYS.TO_DATE:
        try:
            date_from_input_text = datetime.strptime(values[_KEYS.TO_DATE], _CONSTANTS.DATE_FORMAT)
            window[_KEYS.TO_DATE_CALENDAR].calendar_default_date_M_D_Y = (
            date_from_input_text.month,
            date_from_input_text.day,
            date_from_input_text.year,
            )
        except ValueError:
            pass
    

    if event == "Filtrar":
        print("Filtrar")
    elif event == "Ingreso":
        window.hide()
        movement_screen("Ingreso")
        window.UnHide()
        window[_KEYS.TBL_MOVEMENTS].update(values=load_table_data())
    elif event == "Gasto":
        window.hide()
        movement_screen("Gasto")
        window.UnHide()
        window[_KEYS.TBL_MOVEMENTS].update(values=load_table_data())
    elif event == "Categoria":
        window.hide()
        category_screen()
        window.UnHide()

window.close()
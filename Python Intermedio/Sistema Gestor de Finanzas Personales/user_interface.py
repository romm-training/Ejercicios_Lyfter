import FreeSimpleGUI as sg
from datetime import datetime

from dto import category_dto, movement_dto
from business import category_biz, movement_biz

class _CONSTANTS():
    DATE_FORMAT = "%d/%m/%Y"
    COMBO_DEFAULT_VALUE = "--Seleccione--"
    AMOUNT_REGEX = r"^\d+(\.\d{1,2})?$"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'.")

class _FIELD_KEYS():
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

# Llama a la logica de negocio para agregar un movimiento
def movement_call_add_data(values):
    movement = movement_dto.Movement_Dto(
        values[_FIELD_KEYS.MOVEMENT_DATE], 
        values[_FIELD_KEYS.MOVEMENT_TYPE],
        values[_FIELD_KEYS.MOVEMENT_CATEGORY],
        values[_FIELD_KEYS.MOVEMENT_DESCRIPTION],
        values[_FIELD_KEYS.MOVEMENT_AMOUNT]
    )
    
    movement_biz.Movement_Biz().add_data(movement)

# Limpia y establece los campos de la pantalla de movimientos
def movement_clear_fields(window):
    window[_FIELD_KEYS.MOVEMENT_DATE].update("")
    window[_FIELD_KEYS.MOVEMENT_DATE_CALENDAR].calendar_default_date_M_D_Y = (
        datetime.today().month,
        datetime.today().day,
        datetime.today().year
    )
    window[_FIELD_KEYS.MOVEMENT_CATEGORY].update(_CONSTANTS.COMBO_DEFAULT_VALUE)
    window[_FIELD_KEYS.MOVEMENT_AMOUNT].update("")
    window[_FIELD_KEYS.MOVEMENT_DESCRIPTION].update("")

def movement_screen(movement_type):
    categories = category_biz.Category_Biz().read_data()

    filtered_categories = sorted([c.name for c in categories if c.movement_type == movement_type])

    cat_to_show = [_CONSTANTS.COMBO_DEFAULT_VALUE] + filtered_categories

    layout = [
        [sg.Text("Agregar un Movimiento")],
        [
            sg.Text("Tipo: "), 
            sg.InputText(
                movement_type, 
                key=_FIELD_KEYS.MOVEMENT_TYPE, 
                disabled=True
            )
        ],
        [
            sg.Text(f"Fecha: "), 
            sg.InputText(
                "", 
                key=_FIELD_KEYS.MOVEMENT_DATE, 
                size=(12,1), 
                readonly=True, 
                enable_events=True
            ), 
            sg.CalendarButton(
                "📅", 
                key=_FIELD_KEYS.MOVEMENT_DATE_CALENDAR, 
                target=_FIELD_KEYS.MOVEMENT_DATE, 
                format=_CONSTANTS.DATE_FORMAT, 
                no_titlebar=False
            )
        ],
        [
            sg.Text("Categoria: "), 
            sg.Combo(
                values=cat_to_show, 
                key=_FIELD_KEYS.MOVEMENT_CATEGORY, 
                default_value=_CONSTANTS.COMBO_DEFAULT_VALUE
            )
        ],
        [
            sg.Text("Descripcion: "), 
            sg.InputText(key=_FIELD_KEYS.MOVEMENT_DESCRIPTION)
        ],
        [
            sg.Text("Amount: "), 
            sg.InputText(
                key=_FIELD_KEYS.MOVEMENT_AMOUNT,
                size=(15,1)
            )
        ],
        [sg.Button("Guardar"),sg.Button("Cancelar")]
    ]

    window = sg.Window("Agregar Movimientos", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        # Obtiene el valor del textbox, convierte a fecha y se establece el default del calendario. Si es vacio, se asigna la fecha actual.
        if event == _FIELD_KEYS.MOVEMENT_DATE:
            try:
                date_from_input_text = datetime.strptime(
                    values[_FIELD_KEYS.MOVEMENT_DATE], 
                    _CONSTANTS.DATE_FORMAT
                )
                window[_FIELD_KEYS.MOVEMENT_DATE_CALENDAR].calendar_default_date_M_D_Y = (
                    date_from_input_text.month,
                    date_from_input_text.day,
                    date_from_input_text.year,
                )
            except ValueError:
                pass

        # Se aplican las validaciones. Si hay errores, se muestran. Si no, se obtienen los valores, se crea el DTO, se envia a guardar y se limpian los campos.
        if event == "Guardar":
            errors = movement_biz.Movement_Biz().movement_validations(values)
            if len(errors) > 0:
                sg.popup_ok("\n".join(errors))
                continue
            else:
                movement_call_add_data(values)
            
            movement_clear_fields(window)

        if event == "Cancelar":
            movement_clear_fields(window)

    window.close()

# Llama a la logica de negocio que agrega una categoria.
def category_call_add_data(values):
    category = category_dto.Category_Dto(
        values[_FIELD_KEYS.CATEGORY_TYPE], 
        values[_FIELD_KEYS.CATEGORY_NAME],
        values[_FIELD_KEYS.CATEGORY_COLOR]
    )

    category_biz.Category_Biz().add_data(category)

# Limpia los campos de la pantalla de categoria.
def category_clear_fields(window):
    window[_FIELD_KEYS.CATEGORY_TYPE].update(_CONSTANTS.COMBO_DEFAULT_VALUE)
    window[_FIELD_KEYS.CATEGORY_NAME].update("")
    window[_FIELD_KEYS.CATEGORY_COLOR].update("")
    
# Pantalla de Categoría
def category_screen():
    layout = [
            [
                sg.Text("Agregar una Categoria")
            ],
            [
                sg.Text("Tipo: "), 
                sg.Combo(
                    values=[
                        _CONSTANTS.COMBO_DEFAULT_VALUE, 
                        "Ingreso",
                        "Gasto"
                    ], 
                    key=_FIELD_KEYS.CATEGORY_TYPE, 
                    default_value=_CONSTANTS.COMBO_DEFAULT_VALUE
                )
            ],
            [
                sg.Text("Nombre: "), 
                sg.InputText(
                    "", 
                    key=_FIELD_KEYS.CATEGORY_NAME
                )
            ],
            [
                sg.Text("Color: "), 
                sg.Input(
                    key=_FIELD_KEYS.CATEGORY_COLOR, 
                    size=(10,1)
                ), 
                sg.ColorChooserButton("Elegir")
            ],
            [
                sg.Button("Guardar"),
                sg.Button("Cancelar")
            ]
        ]

    window = sg.Window("Ingresar Categorias", layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Guardar":
            errors = category_biz.Category_Biz().category_validations(values)
            if len(errors) > 0:
                sg.popup_ok("\n".join(errors))
                continue
            else:
                category_call_add_data(values)

            category_clear_fields(window)

        if event == "Cancelar":
            category_clear_fields(window)

    window.close()

# Carga los datos del csv. Valida el rango de fechas y aplica filtro si corresponde. Se da formato, se ordena y retorna la lista a mostrar en la tabla.
def load_table_data(from_date=None, to_date=None):
    movements_data = movement_biz.Movement_Biz().read_data()
    if from_date or to_date:
        movements_data = [m for m in movements_data
                          if (from_date is None or datetime.strptime(m.date, _CONSTANTS.DATE_FORMAT) >= from_date)
                          and (to_date is None or datetime.strptime(m.date, _CONSTANTS.DATE_FORMAT) <= to_date)
                          ]
        
    data_list = sorted(
        [
            [m.date, m.type, m.category, m.description, m.amount] for m in movements_data
        ], 
        key=lambda row: datetime.strptime(
            row[0], 
            _CONSTANTS.DATE_FORMAT
        )
    )

    return data_list

layout = [
    [
        sg.Text("Gestor de Finanzas Personales")
    ],
    [
        sg.Text("Fecha Inicial: "), 
        sg.InputText(
            "", 
            key=_FIELD_KEYS.FROM_DATE, 
            size=(11,1), 
            enable_events=True, 
            readonly=True
        ), 
        sg.CalendarButton(
            "📅", 
            key=_FIELD_KEYS.FROM_DATE_CALENDAR, 
            target=_FIELD_KEYS.FROM_DATE, 
            format=_CONSTANTS.DATE_FORMAT, 
            no_titlebar=False, 
            close_when_date_chosen=True
        ), 
        sg.Text(
            "Fecha Final: "), 
            sg.InputText(
                "", 
                key=_FIELD_KEYS.TO_DATE, 
                size=(11,1), 
                enable_events=True, 
                readonly=True
            ), 
            sg.CalendarButton(
                "📅", 
                key=_FIELD_KEYS.TO_DATE_CALENDAR, 
                target=_FIELD_KEYS.TO_DATE, 
                format=_CONSTANTS.DATE_FORMAT,
                no_titlebar=False, 
                close_when_date_chosen=True
            ), 
            sg.Button("Filtrar")
    ],
    [
        sg.Table(
            values=load_table_data(),
            headings=["Fecha","Tipo","Categoria","Descripcion","Monto"],
            auto_size_columns=True,
            key=_FIELD_KEYS.TBL_MOVEMENTS, 
            justification="center"
        )
    ],
    [
        sg.Button("Ingreso"), 
        sg.Button("Gasto"), 
        sg.Button("Categoria")
    ]
]

window = sg.Window("Gestor de Finanzas Personales", layout)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    # Si hay valor en el textbox, se actualiza el valor en el calendario.
    if event == _FIELD_KEYS.FROM_DATE:
        try:
            date_from_input_text = datetime.strptime(
                values[_FIELD_KEYS.FROM_DATE], 
                _CONSTANTS.DATE_FORMAT
            )
            window[_FIELD_KEYS.FROM_DATE_CALENDAR].calendar_default_date_M_D_Y = (
                date_from_input_text.month,
                date_from_input_text.day,
                date_from_input_text.year,
            )
        except ValueError:
            pass

    # Si hay valor en el textbox, se actualiza el valor en el calendario.
    if event == _FIELD_KEYS.TO_DATE:
        try:
            date_from_input_text = datetime.strptime(
                values[_FIELD_KEYS.TO_DATE], 
                _CONSTANTS.DATE_FORMAT
            )
            window[_FIELD_KEYS.TO_DATE_CALENDAR].calendar_default_date_M_D_Y = (
                date_from_input_text.month,
                date_from_input_text.day,
                date_from_input_text.year,
            )
        except ValueError:
            pass

    # Se obtienen los valores, se parsean a fecha y se carga la lista filtrada.
    if event == "Filtrar":
        from_date_input_text = values[_FIELD_KEYS.FROM_DATE]
        to_date_input_text = values[_FIELD_KEYS.TO_DATE]

        if not from_date_input_text or not to_date_input_text:
            sg.popup_ok("Debe seleccionar la fecha inicial y final antes de filtrar.")
        else:
            try:
                var_from_date = datetime.strptime(
                    values[_FIELD_KEYS.FROM_DATE],
                    _CONSTANTS.DATE_FORMAT
                )
                var_to_date = datetime.strptime(
                    values[_FIELD_KEYS.TO_DATE],
                    _CONSTANTS.DATE_FORMAT
                )

                if var_from_date > var_to_date:
                    sg.popup_ok("La fecha inicial no puede ser mayor que la fecha final.")
                    continue

                window[_FIELD_KEYS.TBL_MOVEMENTS].update(values=load_table_data(var_from_date, var_to_date))
            except ValueError:
                sg.popup_ok("Formato de fechas invalido.")

    elif event == "Ingreso":
        window.hide()
        movement_screen("Ingreso")
        window.UnHide()
        window[_FIELD_KEYS.TBL_MOVEMENTS].update(values=load_table_data())
    elif event == "Gasto":
        window.hide()
        movement_screen("Gasto")
        window.UnHide()
        window[_FIELD_KEYS.TBL_MOVEMENTS].update(values=load_table_data())
    elif event == "Categoria":
        window.hide()
        category_screen()
        window.UnHide()

window.close()
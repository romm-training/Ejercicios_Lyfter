from utils import clear_screen, print_exception_message, press_enter_key_to_return_to_main_menu
from actions import enter_students_information, get_all_students, print_all_students, get_top3_students, get_overall_average, get_students_below_passing_grade, get_headers, set_students_from_list, delete_student, is_students_list_empty
from data import write_csv_file, read_csv_file

_MENU = {
    1: "Ingresar información de estudiantes",
    2: "Ver información de los estudiantes ingresados",
    3: "Ver top 3 de estudiantes con mejor promedio",
    4: "Ver promedio general",
    5: "Exportar datos a un archivo CSV",
    6: "Importar datos desde un archivo CSV",
    7: "Ver estudiantes reprobados",
    8: "Eliminar información de un estudiante",
    0: "Salir"
}

def print_menu():
    print("** Menú Principal **")
    print("")
    for key, value in _MENU.items():
        print(f"{key}. {value}")
    print("")

def action_input():
    flow_control = 1
    while flow_control == 1:
        clear_screen()
        print_menu()
        try:
            action = int(input("Ingrese una opción: "))
            if action not in _MENU:
                raise ValueError
            flow_control = 0
        except ValueError:
            print_exception_message("Opción invalida. Intente de nuevo")

    return action

def call_action(action):
    clear_screen()
    match action:
        case 1:
            enter_students_information()
        case 2:
            print_all_students()
        case 3:
            get_top3_students()
        case 4:
            get_overall_average()
        case 5:
            if is_students_list_empty():
                return
            write_csv_file(get_all_students(), get_headers())
        case 6:
            if is_students_list_empty(False):
                set_students_from_list(read_csv_file())
            else:
                print_exception_message("Atención: ya existen datos de estudiantes ingresados o cargados. No se puede cargar del archivo.", False)
                press_enter_key_to_return_to_main_menu()
        case 7:
            get_students_below_passing_grade()
        case 8:
            delete_student()

def main_menu():
    flow_control = 1
    while flow_control == 1:
        action = action_input()

        if action == 0:
            flow_control = 0
        else:
            call_action(action)

    clear_screen()
    print("Saliendo del sistema...")
    print("Gracias por usar el Sistema de Control de Estudiantes")

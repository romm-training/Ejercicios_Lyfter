from utils import clear_screen, print_exception_message
from actions import enter_students_information, print_students

MENU = {
    1: "Ingresar información de estudiantes",
    2: "Ver información de los estudiantes ingresados",
    3: "Ver top 3 de estudiantes con mejor promedio",
    4: "Ver promedio general",
    5: "Exportar datos a un archivo CSV",
    6: "Importar datos desde un archivo CSV",
    0: "Salir"
}

def print_menu():
    for key, value in MENU.items():
        print(f"{key}. {value}")

def action_input():
    flow_control = 1
    while flow_control == 1:
        clear_screen()
        print_menu()
        try:
            action = int(input("Ingrese una opción: "))
            if action not in MENU:
                raise ValueError
            flow_control = 0
        except ValueError:
            print_exception_message("Opción invalida. Intente de nuevo")

    return action

def call_action(action):
    match action:
        case 1:
            enter_students_information()
        case 2:
            print_students()
        case 3:
            print("Opcion 3")
        case 4:
            print("Opcion 4")
        case 5:
            print("Opcion 5")
        case 6:
            print("Opcion 6")

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

from utils import clear_screen, print_exception_message, press_any_key_to_return_to_main_menu
import re

_students = []
_FLOW_CONTROL_INPUT_MESSAGE = "Presione 1 para ingresar la información de otro estudiante o 0 para volver al Menú Principal."
_INVALID_OPTION_MESSAGE = "Opción invalida. Intente de nuevo."
_INTEGER_NUMBER_MESSAGE = "Debe ingresar un número entero."
_DECIMAL_NUMBER_MESSAGE = "Debe ingresar un número entero o decimal entre 0 y 100."

def grade_input(label):
    grade = 0
    while True:
        try:
            grade = float(input(label))
            if not (0 <= grade <= 100):
                raise ValueError()
            return grade
        except ValueError:
            print_exception_message(f"{_DECIMAL_NUMBER_MESSAGE}")
    
    

def string_fullname_input(label):
    string_input = ""
    while True:
        try:
            string_input = input(label)
            if len(string_input) == 0:
                raise ValueError("No se puede ingresar un nombre vacío.")
            
            if re.search(r"\d", string_input):
                raise ValueError("El nombre completo no puede tener números.")

            break
        except ValueError as ex:
            print_exception_message(f"{ex} Intente de nuevo.")

    return string_input

def string_grade_input(label):
    string_input = ""
    # ^ inicio del string
    # \d{1,2} al inicio del string permita 1 o 2 digitos
    # [A-Z]$ una sola letra mayuscula al final
    classroom_pattern = r"^\d{1,2}[A-Z]$"
    while True:
        try:
            string_input = input(label)
            len_input = len(string_input)
            if not re.match(classroom_pattern,string_input):
                raise ValueError("El formato de la clase es incorrecto. Debe iniciar con uno o dos dígitos y terminar con una mayúscula. Por ejemplo, 7B, 12C.")
            break
        except ValueError as ex:
            print_exception_message(f"{ex} Intente de nuevo.")

    return string_input

def _add_student_to_list(student):
    _students.append(student)

def print_students():
    print(_students)
    press_any_key_to_return_to_main_menu()

def enter_students_information():
    flow_control = 1
    
    while flow_control == 1:
        clear_screen()
        student = {}
        print("Ingrese la Información de un Estudiante")
        student["fullName"] = string_fullname_input("Nombre completo: ")
        student["classroom"] = string_grade_input("Sección: ")
        spanish_grade = grade_input("Nota de Español: ")
        student["spanishGrade"] = spanish_grade
        english_grade = grade_input("Nota de Inglés: ")
        student["englishGrade"] = english_grade
        social_studies_grade = grade_input("Nota de Estudios Sociales: ")
        student["socialStudiesGrade"] = social_studies_grade
        science_grade = grade_input("Nota de Ciencias: ")
        student["scienceGrade"] = science_grade
        student["average"] = (spanish_grade + english_grade + social_studies_grade + science_grade) / 4

        while True:
            try:
                save_control = int(input("Digite 1 para salvar o 0 para descartar: "))

                match save_control:
                    case 1:
                        _add_student_to_list(student)
                        print("Información guardada exitosamente.")
                    case 0:
                        break
                    case _:
                        raise ValueError
                break
            except ValueError:
                print_exception_message(f"{_INVALID_OPTION_MESSAGE}")

        while True:
            try:
                flow_control = int(input(_FLOW_CONTROL_INPUT_MESSAGE))
            
                if flow_control not in (0,1):
                    print_exception_message(f"{_INVALID_OPTION_MESSAGE} {_FLOW_CONTROL_INPUT_MESSAGE}.")
            except ValueError as ex:
                print_exception_message(f"{ex}")
            
            break
        




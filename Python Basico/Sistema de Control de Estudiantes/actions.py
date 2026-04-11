from utils import clear_screen, print_exception_message, press_enter_key_to_return_to_main_menu, print_success_message
import re

_students = []
_FLOW_CONTROL_INPUT_MESSAGE = "Presione 1 para ingresar la información de otro estudiante o 0 para volver al Menú Principal: "
_INVALID_OPTION_MESSAGE = "Opción invalida. Intente de nuevo."
_INTEGER_NUMBER_MESSAGE = "Debe ingresar un número entero."
_DECIMAL_NUMBER_MESSAGE = "Debe ingresar un número entero o decimal entre 0 y 100."
_MINIMUM_GRADE_TO_APPROVE = 65
_APPROVED_STATUS = "Aprobado"
_FAILED_STATUS = "Reprobado"
_COLUMN_SETTINGS = {
        "Nombre Completo": 30,
        "Sección": 10,
        "Nota Español": 20 ,
        "Nota Inglés": 20,
        "Nota Est. Sociales": 20,
        "Nota Ciencias": 20,
        "Promedio": 15,
        "Estado": 10
    }
_STUDENT_FIELDS = [
    "fullName",
    "classroom",
    "spanishGrade",
    "englishGrade",
    "socialStudiesGrade",
    "scienceGrade",
    "average",
    "status",
]

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

def _print_students(students):

    for title, tit_len in _COLUMN_SETTINGS.items():
        print(f"{title:<{tit_len}}",end="")
    
    print("")
    print("-" * 145)

    for student in students:
        print(f"{student[_STUDENT_FIELDS[0]]:<{_COLUMN_SETTINGS["Nombre Completo"]}}"
              f"{student[_STUDENT_FIELDS[1]]:<{_COLUMN_SETTINGS["Sección"]}}"
              f"{student[_STUDENT_FIELDS[2]]:<{_COLUMN_SETTINGS["Nota Español"]}}"
              f"{student[_STUDENT_FIELDS[3]]:<{_COLUMN_SETTINGS["Nota Inglés"]}}"
              f"{student[_STUDENT_FIELDS[4]]:<{_COLUMN_SETTINGS["Nota Est. Sociales"]}}"
              f"{student[_STUDENT_FIELDS[5]]:<{_COLUMN_SETTINGS["Nota Ciencias"]}}"
              f"{student[_STUDENT_FIELDS[6]]:<{_COLUMN_SETTINGS["Promedio"]}}"
              f"{student[_STUDENT_FIELDS[7]]:<{_COLUMN_SETTINGS["Estado"]}}")

    press_enter_key_to_return_to_main_menu()

def get_all_students():
    return _students

def set_students_from_list(students_list):
    global _students 
    _students = students_list.copy()
    print("")

def print_all_students():
    _print_students(_students)

def get_overall_average():
    overal_average = sum(float(e[_STUDENT_FIELDS[6]]) for e in _students) / len(_students)
    print(f"El promedio general es: {overal_average:.2f}") 
    press_enter_key_to_return_to_main_menu()

def get_top3_students():
    temp_students = sorted(_students.copy(), key=lambda x: x[_STUDENT_FIELDS[6]], reverse=True)[:3]
    _print_students(temp_students)

def get_students_below_passing_grade():
    temp_students = [e for e in _students if e[_STUDENT_FIELDS[7]] == _FAILED_STATUS]
    _print_students(temp_students)

def _get_student_status(spanish_grade, english_grade, social_studies_grade, science_grade):
    
    is_approved = all([
        spanish_grade >= _MINIMUM_GRADE_TO_APPROVE,
        english_grade >= _MINIMUM_GRADE_TO_APPROVE,
        social_studies_grade >= _MINIMUM_GRADE_TO_APPROVE,
        science_grade >= _MINIMUM_GRADE_TO_APPROVE
    ])

    return _APPROVED_STATUS if is_approved else _FAILED_STATUS

def _get_student_average(spanish_grade, english_grade, social_studies_grade, science_grade):
    return (spanish_grade + english_grade + social_studies_grade + science_grade) / 4

def get_headers():
    return _STUDENT_FIELDS

def enter_students_information():
    flow_control = 1
    
    while flow_control == 1:
        student = {}
        print("Ingrese la Información de un Estudiante")
        student[_STUDENT_FIELDS[0]] = string_fullname_input("Nombre completo: ")
        student[_STUDENT_FIELDS[1]] = string_grade_input("Sección: ")
        spanish_grade = grade_input("Nota de Español: ")
        student[_STUDENT_FIELDS[2]] = spanish_grade
        english_grade = grade_input("Nota de Inglés: ")
        student[_STUDENT_FIELDS[3]] = english_grade
        social_studies_grade = grade_input("Nota de Estudios Sociales: ")
        student[_STUDENT_FIELDS[4]] = social_studies_grade
        science_grade = grade_input("Nota de Ciencias: ")
        student[_STUDENT_FIELDS[5]] = science_grade
        student[_STUDENT_FIELDS[6]] = _get_student_average(spanish_grade, english_grade, social_studies_grade, science_grade)
        student[_STUDENT_FIELDS[7]] = _get_student_status(spanish_grade, english_grade, social_studies_grade, science_grade)

        while True:
            try:
                save_control = int(input("Digite 1 para salvar o 0 para descartar: "))

                match save_control:
                    case 1:
                        _add_student_to_list(student)
                        print_success_message("Información guardada exitosamente.")
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





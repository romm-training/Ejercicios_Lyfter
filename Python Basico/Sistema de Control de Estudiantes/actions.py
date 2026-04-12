from utils import clear_screen, print_exception_message, press_enter_key_to_return_to_main_menu, print_success_message
import re

_students = []
_FLOW_CONTROL_INPUT_MESSAGE = "Presione 1 para ingresar la información de otro estudiante o 0 para volver al Menú Principal: "
_INVALID_OPTION_MESSAGE = "Opción invalida. Intente de nuevo."
_INTEGER_NUMBER_MESSAGE = "Debe ingresar un número entero."
_DECIMAL_NUMBER_MESSAGE = "Debe ingresar un número entero o decimal entre 0 y 100."
_MINIMUM_GRADE_TO_APPROVE = 60
_APPROVED_STATUS = "Aprobado"
_FAILED_STATUS = "Reprobado"
_IDX_NAME = 0
_IDX_CLASSROOM = 1
_IDX_SPANISH = 2
_IDX_ENGLISH = 3
_IDX_SOCIAL_STUDIES = 4
_IDX_SCIENCE = 5
_IDX_AVERAGE = 6
_IDX_STATUS = 7
_IDX_TITLE = 0
_IDX_LENGHT = 1
_COLUMN_SETTINGS = [
        ("Nombre Completo", 25),
        ("Sección", 8),
        ("Nota Español", 15),
        ("Nota Inglés", 15),
        ("Nota Sociales", 15),
        ("Nota Ciencias", 15),
        ("Promedio", 15),
        ("Estado", 10)
    ]
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

    print("** Lista de Estudiantes **")

    for title, tit_len in _COLUMN_SETTINGS:
        print(f"{title:^{tit_len}}",end="")
    
    print("")
    print("-" * 118)

    for student in students:
        print(f"{student[_STUDENT_FIELDS[_IDX_NAME]]:<{_COLUMN_SETTINGS[_IDX_NAME][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_CLASSROOM]]:^{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_SPANISH]]:^{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_ENGLISH]]:^{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_SOCIAL_STUDIES]]:^{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_SCIENCE]]:^{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_AVERAGE]]:^{_COLUMN_SETTINGS[_IDX_AVERAGE][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_STATUS]]:^{_COLUMN_SETTINGS[_IDX_STATUS][_IDX_LENGHT]}}")

    press_enter_key_to_return_to_main_menu()

def _print_students_below_the_minimum_grade(students):

    print("** Estudiantes Reprobados **")
    print(f"{_COLUMN_SETTINGS[_IDX_NAME][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_NAME][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_LENGHT]}}")
    print("-" * 93)

    for student in students:
        print(f"{student[_STUDENT_FIELDS[_IDX_NAME]]:^{_COLUMN_SETTINGS[_IDX_NAME][_IDX_LENGHT]}}"
              f"{student[_STUDENT_FIELDS[_IDX_CLASSROOM]]:^{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_LENGHT]}}",end="")
        spanish_grade = str(student[_STUDENT_FIELDS[_IDX_SPANISH]]) if float(student[_STUDENT_FIELDS[_IDX_SPANISH]]) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{spanish_grade:^{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_LENGHT]}}",end="")
        english_grade = str(student[_STUDENT_FIELDS[_IDX_ENGLISH]]) if float(student[_STUDENT_FIELDS[_IDX_ENGLISH]]) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{english_grade:^{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_LENGHT]}}",end="")
        social_studies_grade = str(student[_STUDENT_FIELDS[_IDX_SOCIAL_STUDIES]]) if float(student[_STUDENT_FIELDS[_IDX_SOCIAL_STUDIES]]) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{social_studies_grade:^{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_LENGHT]}}",end="")
        science_grade = student[_STUDENT_FIELDS[_IDX_SCIENCE]] if float(student[_STUDENT_FIELDS[_IDX_SCIENCE]]) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{science_grade:^{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_LENGHT]}}")

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
    overal_average = sum(float(e[_STUDENT_FIELDS[_IDX_AVERAGE]]) for e in _students) / len(_students)
    print(f"El promedio general es: {overal_average:.2f}") 
    press_enter_key_to_return_to_main_menu()

def get_top3_students():
    temp_students = sorted(_students.copy(), key=lambda x: x[_STUDENT_FIELDS[_IDX_AVERAGE]], reverse=True)[:3]
    _print_students(temp_students)

def get_students_below_passing_grade():
    temp_students = [e for e in _students if e[_STUDENT_FIELDS[_IDX_STATUS]] == _FAILED_STATUS]
    _print_students_below_the_minimum_grade(temp_students)

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

def delete_student():
    fullName = string_fullname_input("Nombre completo: ")
    classroom = string_grade_input("Sección: ")

    confirmation = input(f"Confirma que desea eliminar la información de {fullName} de la sección {classroom}? 1=SI 0=NO: " )

    if confirmation == 1:
        for student in _students:
            if student["fullName"] == fullName and student[classroom] == "classroom":
                _students.remove(student)
                break

def enter_option_0_1(message):
    while True:
        try:
            option = int(input(message))

            if option not in (0,1):
                raise ValueError()
            break
        except ValueError:
            print_exception_message(f"{_INVALID_OPTION_MESSAGE}")
    
    return True, option

def enter_students_information():
    flow_control = 1
    
    while flow_control == 1:
        student = {}
        print("Ingrese la Información de un Estudiante")
        student[_STUDENT_FIELDS[_IDX_NAME]] = string_fullname_input("Nombre completo: ")
        student[_STUDENT_FIELDS[_IDX_CLASSROOM]] = string_grade_input("Sección: ")
        spanish_grade = grade_input("Nota de Español: ")
        student[_STUDENT_FIELDS[_IDX_SPANISH]] = spanish_grade
        english_grade = grade_input("Nota de Inglés: ")
        student[_STUDENT_FIELDS[_IDX_ENGLISH]] = english_grade
        social_studies_grade = grade_input("Nota de Estudios Sociales: ")
        student[_STUDENT_FIELDS[_IDX_SOCIAL_STUDIES]] = social_studies_grade
        science_grade = grade_input("Nota de Ciencias: ")
        student[_STUDENT_FIELDS[_IDX_SCIENCE]] = science_grade
        student[_STUDENT_FIELDS[_IDX_AVERAGE]] = _get_student_average(spanish_grade, english_grade, social_studies_grade, science_grade)
        student[_STUDENT_FIELDS[_IDX_STATUS]] = _get_student_status(spanish_grade, english_grade, social_studies_grade, science_grade)

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





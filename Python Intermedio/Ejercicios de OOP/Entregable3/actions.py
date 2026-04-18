from utils import clear_screen, print_exception_message, press_enter_key_to_return_to_main_menu, print_success_message, press_enter_key_to_return_to_continue
import re

_FLOW_CONTROL_INPUT_MESSAGE = "Presione 1 para ingresar la información de otro estudiante o 0 para volver al Menú Principal: "
_INVALID_OPTION_MESSAGE = "Opción invalida. Intente de nuevo."
_INTEGER_NUMBER_MESSAGE = "Debe ingresar un número entero."
_DECIMAL_NUMBER_MESSAGE = "Debe ingresar un número entero o decimal entre 0 y 100."
_STUDENTS_LIST_EMPTY_MESSAGE = "La lista de estudiantes está vacía. Se debe ingresar información de estudiantes para ejecutar la acción seleccionada."
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
    "full_name",
    "classroom",
    "spanish_grade",
    "english_grade",
    "social_studies_grade",
    "science_grade",
    "average",
    "status",
]

class Student:
    def __init__(self, full_name, classroom, spanish_grade, english_grade, social_studies_grade, science_grade):
        self.full_name = full_name
        self.classroom = classroom
        self.spanish_grade = spanish_grade
        self.english_grade = english_grade
        self.social_studies_grade = social_studies_grade
        self.science_grade = science_grade
        self.average = _get_student_average(spanish_grade, english_grade, social_studies_grade, science_grade)
        self.status = _get_student_status(spanish_grade, english_grade, social_studies_grade, science_grade)

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

def string_classroom_input(label):
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

def _add_student_to_list(students, student):
    students.append(student)
    return students

def _print_students(students):

    print("")
    print("** Lista de Estudiantes **")
    print("")

    for title, tit_len in _COLUMN_SETTINGS:
        print(f"{title:^{tit_len}}",end="")
    
    print("")
    print("-" * 118)

    for student in students:
        print(f"{student.full_name:<{_COLUMN_SETTINGS[_IDX_NAME][_IDX_LENGHT]}}"
              f"{student.classroom:^{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_LENGHT]}}"
              f"{student.spanish_grade:^{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_LENGHT]}}"
              f"{student.english_grade:^{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_LENGHT]}}"
              f"{student.social_studies_grade:^{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_LENGHT]}}"
              f"{student.science_grade:^{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_LENGHT]}}"
              f"{student.average:^{_COLUMN_SETTINGS[_IDX_AVERAGE][_IDX_LENGHT]}}"
              f"{student.status:^{_COLUMN_SETTINGS[_IDX_STATUS][_IDX_LENGHT]}}")

    press_enter_key_to_return_to_main_menu()

def _print_students_below_the_minimum_grade(students):
    if is_students_list_empty(students):
        return
    
    print("** Estudiantes Reprobados **")
    print("")
    print(f"{_COLUMN_SETTINGS[_IDX_NAME][_IDX_TITLE]:<{_COLUMN_SETTINGS[_IDX_NAME][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_LENGHT]}}",end="")
    print(f"{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_TITLE]:^{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_LENGHT]}}")
    print("-" * 93)

    for student in students:
        print(f"{student.full_name:<{_COLUMN_SETTINGS[_IDX_NAME][_IDX_LENGHT]}}"
              f"{student.classroom:^{_COLUMN_SETTINGS[_IDX_CLASSROOM][_IDX_LENGHT]}}",end="")
        spanish_grade = str(student.spanish_grade) if float(student.spanish_grade) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{spanish_grade:^{_COLUMN_SETTINGS[_IDX_SPANISH][_IDX_LENGHT]}}",end="")
        english_grade = str(student.english_grade) if float(student.english_grade) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{english_grade:^{_COLUMN_SETTINGS[_IDX_ENGLISH][_IDX_LENGHT]}}",end="")
        social_studies_grade = str(student.social_studies_grade) if float(student.social_studies_grade) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{social_studies_grade:^{_COLUMN_SETTINGS[_IDX_SOCIAL_STUDIES][_IDX_LENGHT]}}",end="")
        science_grade = student.science_grade if float(student.science_grade) < _MINIMUM_GRADE_TO_APPROVE else "-"
        print(f"{science_grade:^{_COLUMN_SETTINGS[_IDX_SCIENCE][_IDX_LENGHT]}}")

    press_enter_key_to_return_to_main_menu()

def get_all_students(students):
    return students

def set_students_from_list(students, students_list):
    if students_list == None:
        return

    students = students_list.copy()
    print("")
    return students

def print_all_students(students):
    if is_students_list_empty(students):
        return
    _print_students(students)

def get_overall_average(students):
    if is_students_list_empty(students):
        return
    
    overal_average = sum(float(e.average) for e in students) / len(students)
    print(f"El promedio general es: {overal_average:.2f}") 
    press_enter_key_to_return_to_main_menu()

def get_top3_students(students):
    if is_students_list_empty(students):
        return
    temp_students = sorted(students.copy(), key=lambda x: x.average, reverse=True)[:3]
    _print_students(temp_students)

def get_students_below_passing_grade(students):
    if is_students_list_empty(students):
        return
    temp_students = [e for e in students if e.status == _FAILED_STATUS]
    if len(temp_students) == 0:
        print_exception_message("No hay estudiantes reprobados.")
        press_enter_key_to_return_to_main_menu()
        return
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

def delete_student(students):
    if is_students_list_empty(students):
        return

    print("** Eliminar Información de un Estudiante **")
    print("")
    full_name = string_fullname_input("Nombre completo: ")
    classroom = string_classroom_input("Sección: ")
    print("")

    if not if_student_exists(students, full_name, classroom):
        print_exception_message(f"El estudiante no existe: {full_name}, sección {classroom}.", False)
        press_enter_key_to_return_to_main_menu()
        return
    
    confirmation = enter_option_0_1(f"Confirma que desea eliminar la información de '{full_name}' de la sección '{classroom}'? 1=SI 0=NO: " )

    if confirmation == 1:
        for student in students:
            if student.full_name == full_name and student.classroom == classroom:
                students.remove(student)
                print_success_message("Información eliminada correctamente.")
                print("")
                break
    else:
        print("Eliminación cancelada por el usuario.")

    press_enter_key_to_return_to_main_menu()

def enter_option_0_1(message):
    while True:
        try:
            option = int(input(message))

            if option not in (0,1):
                raise ValueError()
            break
        except ValueError:
            print_exception_message(f"{_INVALID_OPTION_MESSAGE} {message}")
    
    return option

def is_students_list_empty(students, show_messages = True):
    validation_result = len(students) == 0

    if validation_result:
        if show_messages:
            print_exception_message(_STUDENTS_LIST_EMPTY_MESSAGE)
            press_enter_key_to_return_to_main_menu()

    return validation_result

def if_student_exists(students, full_name, classroom):
    exists = any(
        e.full_name == full_name and 
        e.classroom == classroom 
        for e in students
    )
    return exists

def enter_students_information(students):
    flow_control = 1
    
    while flow_control == 1:
        clear_screen()
        student = {}
        print("** Información de un Estudiante **")
        print("")
        full_name = string_fullname_input("Nombre completo: ")
        student.fullName = full_name
        classroom = string_classroom_input("Sección: ")
        student.classroom = classroom

        if if_student_exists(students, full_name, classroom):
            print_exception_message(f"El estudiante '{full_name}' de la sección '{classroom}' ya existe.")
            press_enter_key_to_return_to_continue()
            continue

        spanish_grade = grade_input("Nota de Español: ")
        student.spanish_grade = spanish_grade
        english_grade = grade_input("Nota de Inglés: ")
        student.english_grade = english_grade
        social_studies_grade = grade_input("Nota de Estudios Sociales: ")
        student.social_studies_grade = social_studies_grade
        science_grade = grade_input("Nota de Ciencias: ")
        student.science_grade = science_grade
        student.average = _get_student_average(spanish_grade, english_grade, social_studies_grade, science_grade)
        student.status = _get_student_status(spanish_grade, english_grade, social_studies_grade, science_grade)

        while True:
            print("")
            save_control = enter_option_0_1("Digite 1 para salvar o 0 para descartar: ")

            if save_control == 1:
                _add_student_to_list(students, student)
                print_success_message("Información guardada exitosamente.")
            else:
                print_success_message("Información descartada.")
            break
        
        print("")
        flow_control = enter_option_0_1(_FLOW_CONTROL_INPUT_MESSAGE)
    
    return students

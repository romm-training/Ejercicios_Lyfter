import subprocess

def clear_screen():
    subprocess.run("cls",shell=True)

def print_exception_message(message, try_again_message = True):
    if try_again_message:
        print(f"\033[33m{message} Intente de nuevo.\033[0m")
    else:
        print(f"\033[33m{message}\033[0m")

def print_success_message(message):
    print(f"\033[34m{message}\033[0m")

def press_enter_key_to_return_to_main_menu():
    print("")
    any_key = input("Presione Enter para regresar al Menú Principal")

def press_enter_key_to_return_to_continue():
    print("")
    any_key = input("Presione Enter para continuar.")
import subprocess

def clear_screen():
    subprocess.run("cls",shell=True)

def print_exception_message(message):
    print(f"\033[33m{message} Intente de nuevo.\033[0m")

def press_any_key_to_return_to_main_menu():
    any_key = input("Presione cualquier tecla para regresar al Menú Principal")
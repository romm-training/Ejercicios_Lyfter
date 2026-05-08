user_logged_in = False

def requires_login(func):
    def wrapper():
        try:
            if not user_logged_in:
                raise ValueError("Usuario no autenticado")
        except ValueError as e:
            print(f"{e}")
        
        func()

    return wrapper

@requires_login
def view_profile():
    print("Mostrando perfil del usuario")

def main():
    view_profile()
    user_logged_in = True
    view_profile

if __name__ == "__main__":
    main()
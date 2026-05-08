def print_parameters(func):
    def wrapper(*args):
        print("Decorador - Antes ejecutar funcion")
        for index, arg in enumerate(args):
            print(f"Decorador - Parametro {index}: {arg}")

        response_value = func(*args)

        print("Decorador - Despues ejecutar funcion")
        print(f"Decorador - Respuesta: {response_value}")

        return response_value

    return wrapper

@print_parameters
def create_sentence_from_words(*args):
    return " ".join(args)

@print_parameters
def sum_of_numbers(*args):
    return sum(float(a) for a in args)

def main():
    create_sentence_from_words("Ahora","es","un","buen","momento","para","aprender")
    result = sum_of_numbers(10,10,10,15,15,15,20,20,20)
    print(result)

if __name__ == "__main__":
    main()
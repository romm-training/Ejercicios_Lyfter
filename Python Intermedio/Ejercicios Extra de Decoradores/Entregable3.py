from datetime import datetime

def validate_numbers(func):
    def wrapper(open1,oper2):
        try:
            if not isinstance(open1,(int,float)) or not isinstance(oper2,(int,float)):
                raise ValueError()
            return func(open1, oper2)
        except ValueError:
            print(f"Los parametros deben ser numericos.")
    return wrapper

def log_call(func):
    def wrapper(oper1, oper2):
        result = func(oper1, oper2)
        print(f"func:{func.__name__} - args: {oper1}, {oper2} - [{datetime.now()}] - Resultado: {result}")
        return result
    return wrapper

@validate_numbers
@log_call
def multiply(oper1, oper2):
    return oper1 * oper2

def main():
    print(f"Resultado: {multiply(2,5)}")
    print(f"Resultado: {multiply(2,"AB")}")

if __name__ == "__main__":
    main()

class Exception_With_No_Trace(Exception):
    pass

def validate_numeric_parameters(func):
    def wrapper(*args):
        if not all(isinstance(a,(int,float)) for a in args):
            raise Exception_With_No_Trace("Atención, todos los parametros deben ser numericos")

        return func(*args)

    return wrapper

@validate_numeric_parameters
def sum_of_numbers(*args):
    return sum(float(a) for a in args)

def main():
    print(f"Primera suma: {sum_of_numbers(10,20,30,40)}")
    print(f"Segunda suma: {sum_of_numbers(10,20,True,'ABC')}")

if __name__ == "__main__":
    main()
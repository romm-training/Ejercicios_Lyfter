def addition(number1: float, number2: float) -> float:
    return number1 + number2

def substraction(number1: float, number2: float) -> float:
    return number1 - number2

def multiplication(number1: float, number2: float) -> float:
    return number1 * number2

def division(number1: float, number2: float) -> float:
    if number2 == 0:
        raise ValueError("No se puede dividir por cero")
    return number1 / number2

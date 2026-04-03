counter = 1
total = 0
continue_indicator = 1
number = 0

while continue_indicator == 1:
    number = int(input("Ingrese un numero mayor o igual que 1: "))
    if number < 1:
        print("Numero incorrecto.")
    else:
        while counter <= number:
            total = total + counter
            counter = counter + 1
        
        print(f"La suma de numeros de 1 hasta {number} es: {total}" )
    
    continue_indicator = int(input("Desea continuar? 1=SI 0=NO: "))




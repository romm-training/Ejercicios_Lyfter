class Rectangle:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth

    def get_area(self):
        return self.width * self.heigth
    
    def get_perimeter(self):
        return (self.width * 2) + (self.heigth * 2)
    
def main():
    while True:
        heigth = float(input("Ingrese el largo: "))
        if heigth > 0:
            break
        else:
            print("El valor del lado largo no puede ser negativo o 0. Intente de nuevo.")

    while True:
        width = float(input("Ingrese el ancho: "))
        if width > 0:
            if width < heigth:
                break
            else:
                print("El lado ancho debe ser menor que el lado largo. Intente de nuevo.")
        else:
            print("El valor del lado ancho no puede ser negativo o 0. Intente de nuevo.")

    rectangle = Rectangle(heigth, width)

    print(f"Area: {rectangle.get_area():.2f}")
    print(f"Perimetro: {rectangle.get_perimeter():.2f}")

if __name__ == "__main__":
    main()
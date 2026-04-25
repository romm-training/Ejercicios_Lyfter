from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_perimeter(self):
        pass

    @abstractmethod
    def calculate_area(self):
        pass

class Circle(Shape):
    PI = 3.1416
    def __init__(self, radius):
        self.radius = radius

    def calculate_perimeter(self):
        return 2 * self.PI * self.radius
    
    def calculate_area(self):
        return self.radius ** 2 * self.PI
    
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_perimeter(self):
        return 4 * self.side
    
    def calculate_area(self):
        return self.side ** 2

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)
    
    def calculate_area(self):
        return self.length * self.width
    
def main():
    circle = Circle(10)
    print(f"Circulo con radio {circle.radius} -> Area: {circle.calculate_area():.2f} y Perímetro: {circle.calculate_perimeter():.2f} ")
    square = Square(10)
    print(f"Cuadrado con lado {square.side} -> Area: {square.calculate_area():.2f} y Perímetro: {square.calculate_perimeter():.2f} ")
    rectangle = Rectangle(10,5)
    print(f"Rectángulo con largo {rectangle.length} y ancho {rectangle.width} -> Area: {rectangle.calculate_area():.2f} y Perímetro: {rectangle.calculate_perimeter():.2f} ")

if __name__ == "__main__":
    main()
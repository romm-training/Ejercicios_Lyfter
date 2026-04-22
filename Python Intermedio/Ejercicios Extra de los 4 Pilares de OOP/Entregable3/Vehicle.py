class Vehicle:
    def __init__(self, brand, year):
        self._brand = brand
        self._year = year

    def get_info(self):
        return f"Vehículo marca '{self._brand}', año de fabricación '{self._year}'"

class Car(Vehicle):
    def __init__(self, brand, year, doors):
        super().__init__(brand, year)
        self._doors = doors

    def get_info(self):
        return f"{super().get_info()}, cantidad de puertas '{self._doors}'"
    
class Motorcycle(Vehicle):
    def __init__(self, brand, year, type):
        super().__init__(brand, year)
        self._type = type

    def get_info(self):
        return f"{super().get_info()}, tipo '{self._type}'"
    
def main():
    vehicle1 = Car("Toyota",2020,5)
    vehicle2 = Motorcycle("Yamaha",2022,"Deportiva")

    print(vehicle1.get_info())
    print(vehicle2.get_info())

if __name__ == "__main__":
    main()
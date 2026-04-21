class Bus:
    passengers = []
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers

    def add_passenger(self, person):
        if len(self.passengers) >= self.max_passengers:
            print(f"No se puede agregar más pasajeros porque se alcanzó el límite de {self.max_passengers}.")
            return
    
        self.passengers.append(person)

    def remove_passenger(self):
        if len(self.passengers) == 0:
            print(f"No se puede bajar pasajeros porque el autobús está vacío.")
            return
        self.passengers.pop()

    def print_bus(self):
        [print(f"{passenger.name}") for passenger in self.passengers]
        

class Person():
	def __init__(self, name, age):
		self.name = name
		self.age = age

def main():
    the_bus = Bus(3)

    person1 = Person("Juan",21)
    person2 = Person("Padro",22)
    person3 = Person("Maria",23)
    person4 = Person("Ana",24)
    person5 = Person("Ruben",25)

    the_bus.add_passenger(person1)
    the_bus.add_passenger(person2)
    the_bus.add_passenger(person3)
    the_bus.add_passenger(person4)
    the_bus.add_passenger(person5)

    the_bus.print_bus()

    the_bus.remove_passenger()
    the_bus.remove_passenger()
    the_bus.remove_passenger()
    the_bus.remove_passenger()
    the_bus.remove_passenger()

if __name__ == "__main__":
    main()
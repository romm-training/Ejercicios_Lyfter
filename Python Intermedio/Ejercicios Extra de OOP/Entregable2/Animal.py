class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Hace un sonido"
    
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def speak(self):
        return "Guau"
    
class Cat(Animal):
    def __init__(self, name):
        super().__init__(name)

    def speak(self):
        return "Miau"
    
def main():
    dog = Dog("Koki")
    print(f"{dog.name} hace el sonido {dog.speak()}")
    cat = Cat("Koki")
    print(f"{cat.name} hace el sonido {cat.speak()}")

if __name__ == "__main__":
    main()
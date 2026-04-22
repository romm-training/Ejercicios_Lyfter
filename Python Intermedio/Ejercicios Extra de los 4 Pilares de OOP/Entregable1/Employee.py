class Employee:
    def __init__(self, name, salary):
        self._name = name
        self._salary = salary

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("El nombre no puede estar vacio")
        self._name = name
    
    @property
    def salary(self):
        return self.salary
    
    @salary.setter
    def salary(self, salary):
        if salary < 0:
            raise ValueError("El salario no puede ser negativo.")
        self._salary = salary

    def promote(self, percentage):
        self._salary = self._salary * (1 + percentage)

    def __str__(self):
        return f"Nombre: {self._name}, Salario: {self._salary}"

def main():
    emp = Employee("Juan", 1000)
    print(str(emp))
    emp.promote(0.2)
    print(str(emp))


if __name__ == "__main__":
    main()
class Circle():
    pi = 3.1416
    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return self.radius**2 * self.pi
    
def main():
    my_circle = Circle(5)
    print(f"{my_circle.get_area():.2f}")

if __name__ == "__main__":
    main()
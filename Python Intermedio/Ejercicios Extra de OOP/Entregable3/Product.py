class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def show_products(self):
        [print(p.__dict__) for p in self.products]

    def calculate_total_value_of_inventory(self):
        return sum([p.price * p.quantity for p in self.products])
    
def main():
    prd1 = Product("Mouse",25,5)
    prd2 = Product("Teclado",50,5)
    prd3 = Product("Monitor",150,3)

    inv = Inventory()
    inv.add_product(prd1)
    inv.add_product(prd2)
    inv.add_product(prd3)

    inv.show_products()

    print(f"Valor total del inventario: {inv.calculate_total_value_of_inventory():.2f}")

if __name__ == "__main__":
    main()
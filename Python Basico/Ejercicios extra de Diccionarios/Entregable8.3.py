products = [
    {"name": "Monitor", "category": "Electrónica", "price": 200},
    {"name": "Teclado", "category": "Electrónica", "price": 50},
    {"name": "Silla", "category": "Muebles", "price": 120},
    {"name": "Mesa", "category": "Muebles", "price": 180},
    {"name": "Mouse", "category": "Electrónica", "price": 25},
    {"name": "Olla Arrocera", "category": "Linea Blanca", "price": 80},
    {"name": "Olla Presion", "category": "Linea Blanca", "price": 90},
]

categories = []
category_exists = False

for product in products:
    temp_category = product["category"]
    temp_price = product["price"]

    if len(categories) == 0:
        categories.append({temp_category: temp_price})
    else:
        for category in categories:
            if category.get(temp_category) != None:
                category[temp_category] = category[temp_category] + temp_price
                category_exists = True
                break

        if not category_exists:
            categories.append({temp_category: temp_price})

    category_exists = False

print(categories)
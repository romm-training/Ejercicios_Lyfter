threshold_price = 100
price = float(input("Ingrese el precio del producto:"))
standard_discount_percentage = 0.02
premium_discount_percentage = 0.1
discount = 0
if price < threshold_price:
    discount = price * standard_discount_percentage
else:
    discount = price * premium_discount_percentage

final_price = price - discount

print(f"El precio final es {final_price:.2f}")
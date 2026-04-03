my_list = [-9,4,-7,1,5]
smallest = my_list[0]

for number in my_list:
    if number < smallest:
        smallest = number

print(f"El numero menor es: {smallest}")
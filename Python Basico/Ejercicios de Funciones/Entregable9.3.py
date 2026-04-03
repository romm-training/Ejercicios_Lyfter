my_list = [4, 6, 2, 29]

def sum_list(list):
    total = 0
    for num in list:
        total = total + num
    return total

def sum_list_2(list):
    return sum(list)
    
print(f"La suma de la lista es: {sum_list(my_list)}")
print(f"La suma optimizada de la lista es: {sum_list_2(my_list)}")
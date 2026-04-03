my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13]
index = 0

print(f"Lista original: {my_list}")

while index < len(my_list):
    if my_list[index] % 2 != 0:
        my_list.pop(index)
    else:
        index = index + 1 

print(f"Lista sin numeros impares: {my_list}")
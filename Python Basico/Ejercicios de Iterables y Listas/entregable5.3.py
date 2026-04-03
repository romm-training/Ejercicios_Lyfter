#my_list = [4,3,6,1,7]
my_list = [8,5,6,0,4,3,6,1,7,0]

print(f"Lista original: {my_list}")

temporary = my_list[0]
last_element_index = len(my_list)-1
my_list[0] = my_list[last_element_index]
my_list[last_element_index] = temporary

print(f"Lista modificada: {my_list}")
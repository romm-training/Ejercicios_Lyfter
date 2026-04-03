list_a = ["first_name", "last_name", "role"]
list_b = ["Alek", "Castillo", "Software Engineer"]

my_dictionary = {}

for index in range(0,len(list_a)):
    my_dictionary[list_a[index]] = list_b[index]

print(my_dictionary)
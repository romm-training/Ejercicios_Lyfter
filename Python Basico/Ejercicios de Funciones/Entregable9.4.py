def reverse_a_string(str):
    new_string = ""
    for index in range(len(str)-1,-1,-1):
        new_string = new_string + str[index]
    return new_string
    
print(reverse_a_string("Hola mundo"))
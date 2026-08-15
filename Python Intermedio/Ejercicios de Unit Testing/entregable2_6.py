my_string = "python-variable-funcion-computadora-monitor"

def sort_string_alphabetically(str):
    my_list = str.split("-")
    my_list.sort()
    return "-".join(my_list)

print(my_string)
print(sort_string_alphabetically(my_string))
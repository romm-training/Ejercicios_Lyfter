my_string = "I love Nación Sushi"

def count_uppercase_lowercase(str):
    lowercase_count = 0
    uppercase_count = 0
    for char in str:
        if char.isupper():
            uppercase_count = uppercase_count + 1
        elif char.islower():
            lowercase_count = lowercase_count + 1

    print(f"Hay {uppercase_count} mayusculas y {lowercase_count} minusculas")


count_uppercase_lowercase(my_string)
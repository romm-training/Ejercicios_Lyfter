my_list = [5, 25, 47, 6, 70]
total = 0
count = 0

for number in my_list:
    total = total + number
    count = count + 1

average = total / count

new_list = []

for number in my_list:
    if number > average:
        new_list.append(number)

print(f"Promedio: {average}")
print(f"Nueva lista: {new_list}")
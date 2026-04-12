words = []
for index in range(0,5):
    words.append(input("Ingrese una palabra: "))

ref_length = 4
new_list = []

for word in words:
    if len(word) > ref_length:
        new_list.append(word)

if len(new_list) == 0:
    print("No hay palabras que tengan mas de cuatro letras")
else:
    print(new_list)        
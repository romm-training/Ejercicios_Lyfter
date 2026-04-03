def words_larger_than_n(word_list, number_of_letters):
    new_list = []
    for word in word_list:
        if len(word) > number_of_letters:
            new_list.append(word)

    return new_list

list = ["cielo","sol","maravilloso","dia"]

number_of_letters = int(input("Ingrese la cantidad de letras minimas en la palabra: "))
print(words_larger_than_n(list, number_of_letters))
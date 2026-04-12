name = input("Ingrese su nombre: ")
sur_name = input("Ingrese su apellido: ")
age = int(input("Ingrese su edad: "))

baby_age = 2
child_age = 9
preteen_age = 12
teenager_age = 17
young_adult_age = 44
adult = 59
result = "Es un adulto mayor"

if (age <= baby_age):
    result = "Es un bebé"
elif (age <= child_age):
    result = "Es un niño"
elif (age <= preteen_age):
    result = "Es un preadolescente"
elif (age <= teenager_age):
    result = "Es un adolescente"
elif (age <= young_adult_age):
    result = "Es un adulto joven"
elif (age <= adult):
    result = "Es un adulto"

print(result)

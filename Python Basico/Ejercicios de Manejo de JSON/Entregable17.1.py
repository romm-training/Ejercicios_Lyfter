import os, json

DEFAULT_ENCODING = "utf-8"

def read_json_file(file_path):
    with open(file_path, "r", encoding=DEFAULT_ENCODING) as file:
        json_file = json.load(file)

    return json_file

def update_json_file(file_path, data):
    with open(file_path, "w", encoding=DEFAULT_ENCODING) as file:
        json.dump(data, file)


def integer_input(label):
    flow_controller = 0
    int_input = 0
    while flow_controller == 0:
        try:
            int_input = int(input(f"{label}: "))
            flow_controller = 1
        except ValueError:
            print(f"El valor para {label} debe ser número entero.")

    return int_input

def pokemon_input():
    print("Ingrese los datos de un Pokémon")
    print("NOTA: Los campos con '*' son número entero")
    pokemon = {
        "name": {},
        "type": [],
        "base": {}
    }

    pokemon["name"]["english"] = input("Nombre: ") 
    pokemon["level"] = integer_input("Nivel*: ")
    pokemon["type"] = input("Lista de tipos separados por comas: ").split(",")
    pokemon["base"]["HP"] = integer_input("Base HP*: ")
    pokemon["base"]["Attack"] = integer_input("Base Ataque*: ")
    pokemon["base"]["Defense"] = integer_input("Base Defensa*: ")
    pokemon["base"]["Sp. Attack"] = integer_input("Base Ataque SP*: ")
    pokemon["base"]["Sp. Defense"] = integer_input("Base Ataque SP*: ")
    pokemon["base"]["Speed"] = integer_input("Base Velocidad*: ")

    return pokemon

def main():
    file_path = os.path.join(os.path.dirname(__file__),"Pokemons.json")
    pokemons = read_json_file(file_path)
    pokemon = pokemon_input()
    pokemons.append(pokemon)
    update_json_file(file_path,pokemons)

if __name__ == "__main__":
    main()
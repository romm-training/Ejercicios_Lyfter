import os, json

DEFAULT_ENCODING = "utf-8"

def read_json_file(file_path):
    with open(file_path,"r",encoding=DEFAULT_ENCODING) as file:
        pokemons = json.load(file)
    
    return pokemons

def print_pokemons(pokemons, pokemon_type):
    name_title = "Nombre"
    level_title = "Level"
    type_title = "Tipo"
    name_col_len = 30
    level_col_len = 15
    type_col_len = 40

    print(f"{name_title:<{name_col_len}}{level_title:<{level_col_len}}{type_title:<{type_col_len}}")
    print("-" * 85)
    pokemons.sort(key=lambda x:x["name"]["english"])
    for pokemon in pokemons:
        if pokemon_type in pokemon["type"]:
            type_value = ",".join(pokemon["type"])
            print(f"{pokemon["name"]["english"]:<{name_col_len}}{pokemon["level"]:<{level_col_len}}{type_value:<{type_col_len}}")

def ask_for_pokemon_type():
    available_types = ["Electric","Fire","Water"]
    print("Tipos de Pokémon disponibles: ")
    [print(pok_type) for pok_type in available_types]
    flow_control = 0
    while flow_control == 0:
        pokemon_type = input("Ingrese el tipo de Pokemon: ")
        if pokemon_type in available_types:
            flow_control = 1
        else:
            print("El tipo ingresado no es válido. Intente de nuevo")
    return pokemon_type

def main():
    file_path = os.path.join(os.path.dirname(__file__),"Pokemons.json")
    pokemons = read_json_file(file_path)
    pokemon_type = ask_for_pokemon_type()
    print_pokemons(pokemons, pokemon_type)


if __name__ == "__main__":
    main()
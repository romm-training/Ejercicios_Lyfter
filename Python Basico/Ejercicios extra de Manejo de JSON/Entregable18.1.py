import os, json

DEFAULT_ENCODING = "utf-8"

def read_json_file(file_path):
    with open(file_path,"r",encoding=DEFAULT_ENCODING) as file:
        pokemons = json.load(file)
    
    return pokemons

def print_pokemons(pokemons):
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
        type_value = ",".join(pokemon["type"])
        print(f"{pokemon["name"]["english"]:<{name_col_len}}{pokemon["level"]:<{level_col_len}}{type_value:<{type_col_len}}")


def main():
    file_path = os.path.join(os.path.dirname(__file__),"Pokemons.json")
    pokemons = read_json_file(file_path)
    print_pokemons(pokemons)


if __name__ == "__main__":
    main()
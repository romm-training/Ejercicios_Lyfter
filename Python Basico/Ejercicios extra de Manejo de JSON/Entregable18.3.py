import os, json

DEFAULT_ENCODING = "utf-8"

def read_json_file(file_path):
    with open(file_path,"r",encoding=DEFAULT_ENCODING) as file:
        pokemons = json.load(file)
    
    return pokemons

def print_pokemons(pokemons):
    name_title = "Nombre"
    attack_title = "Atqque"
    defense_title = "Defensa"
    speed_title = "Velocidad"
    name_col_len = 30
    attack_col_len = 10
    defense_col_len = 10
    speed_col_len = 10

    print(f"{name_title:<{name_col_len}}"
          f"{attack_title:<{attack_col_len}}"
          f"{defense_title:<{defense_col_len}}"
          f"{speed_title:<{defense_col_len}}"
        )
    print("-" * 60)
    pokemons.sort(key=lambda x:x["name"]["english"])
    for pokemon in pokemons:
        print(f"{pokemon["name"]["english"]:<{name_col_len}}"
              f"{pokemon["base"]["Attack"]:<{attack_col_len}}"
              f"{pokemon["base"]["Defense"]:<{defense_col_len}}"
              f"{pokemon["base"]["Speed"]:<{speed_col_len}}"
              )


def main():
    file_path = os.path.join(os.path.dirname(__file__),"Pokemons.json")
    pokemons = read_json_file(file_path)
    print_pokemons(pokemons)


if __name__ == "__main__":
    main()
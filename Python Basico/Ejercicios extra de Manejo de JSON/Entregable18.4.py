import os, json
from collections import Counter,defaultdict

DEFAULT_ENCODING = "utf-8"

def read_json_file(file_path):
    with open(file_path,"r",encoding=DEFAULT_ENCODING) as file:
        pokemons = json.load(file)
    
    return pokemons

def print_averages_per_type(avg_per_type):
    print(f"Type           Promedio de Nivel")
    print("-" * 32)
    for key,value in avg_per_type.items():
        print(f"{key:<15}{value:.2f}")

"""
Se me dificulto llegar a una solucion optima porque el campo type en el archivo es una lista.
Esto quiere decir, que un pokemon puede pertenecer a uno o mas tipos, y a la hora de sacar promedios y contar hay que recorrer dicha lista.
Lo que hice fue:
. Recorrer todos los pokemones para obtener una lista consolidada de todos los tipos existentes.
. Recorrer la lista de tipos y buscar en todos los pokemones cual pertenece al tipo que estoy iterando para sumar el nivel y contar.
. Calcular el promedio del tipo que se esta iterando y guardarlo en un diccionario.

A pesar de que funciona, me parece que no es eficiente porque hay que iterar dos veces la lista de pokemones. Si esta lista es muy grande, va a afectar el rendimiento.
Intente resolverlo en una sola iteracion con las herramientas que nos han dado hasta ahora, pero no lo logre.
IA recomienda Counter, defaultdict y pandas
"""
def averages_per_type_a(pokemons):
    pok_type_list = []
    for pokemon in pokemons:
        [pok_type_list.append(ptype) for ptype in pokemon["type"] if ptype not in pok_type_list]

    pok_type_list.sort()
    pok_type_average = {}
    
    for ptype in pok_type_list:
        psum = 0
        pcount = 0    
        for pokemon in pokemons:
            if ptype in pokemon["type"]:
                psum = psum + pokemon["level"]
                pcount = pcount + 1
        
        if pcount == 0:
            pok_type_average[ptype] = 0
        else:
            pok_type_average[ptype] = psum / pcount

    return pok_type_average

def averages_per_type_b(pokemons):
    type_count = Counter()
    type_sum = defaultdict(int)
    for pokemon in pokemons:
        for ptype in pokemon["type"]:
            type_count[ptype] += 1
            type_sum[ptype] += pokemon["level"] 

    type_avg = {ptype: type_sum[ptype] / type_count[ptype] for ptype in type_count}

    return type_avg

def main():
    file_path = os.path.join(os.path.dirname(__file__),"Pokemons.json")
    pokemons = read_json_file(file_path)
    avg_per_type = averages_per_type_a(pokemons)
    print_averages_per_type(avg_per_type)
    print("\n\n")
    avg_per_type = averages_per_type_b(pokemons)
    print_averages_per_type(avg_per_type)


if __name__ == "__main__":
    main()
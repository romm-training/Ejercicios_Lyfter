import os,csv
from collections import Counter

DEFAULT_ENCODING = "utf-8"

def read_csv_file(file_path):
    videogames = []
    with open(file_path,"r",encoding=DEFAULT_ENCODING) as file:
        reader = csv.DictReader(file)
        videogames = list(reader)
    
    return videogames

def get_videogames_quantity_by_genre(videogames):
    genre_list = Counter(videogame["genre"] for videogame in videogames)
    #for videogame in videogames:
    #    if videogame["genre"] in genre_list:
    #        videogame["quantity"] = videogame["quantity"] + 1
    #    else:
    #        genre_list.append({"genre":videogame["genre"],"quantity":1})

    return genre_list

def print_list(list_to_print, headers):
    print(f"{headers[0]:<30}{headers[1]:<20}")
    print("-" * 50)
    for element_key, element_value in list_to_print.items():
        print(f"{element_key:<30}{element_value:<20}")

    
def main():
    file_path = os.path.join(os.path.dirname(__file__),"Videojuegos.csv")
    videogames = read_csv_file(file_path)
    genre_list = get_videogames_quantity_by_genre(videogames)
    headers = ["Género","Cantidad"]
    print_list(genre_list, headers)

if __name__ == "__main__":
    main()

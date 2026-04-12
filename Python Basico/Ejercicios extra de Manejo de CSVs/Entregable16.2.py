import os, csv

DEFAULT_ENCODING = "utf-8"

def read_csv_file(file_path):
    videogames = []
    with open(file_path, "r", encoding=DEFAULT_ENCODING) as file:
        reader = csv.DictReader(file)
        videogames = list(reader)

    return videogames

def print_videogames(videogames):
    col_title_name = "Nombre"
    col_title_genre = "Género"
    col_title_dev = "Desarrollador"
    col_name_len = 50
    col_genre_len = 20
    col_dev_len = 30
    print(f"{col_title_name:<{col_name_len}}{col_title_genre:<{col_genre_len}}{col_title_dev:<{col_dev_len}}")
    print("-" * 100)
    [print(f"{videogame["title"]:<{col_name_len}}{videogame["genre"]:<{col_genre_len}}{videogame["developer"]:<{col_dev_len}}") 
     for videogame in videogames]
    

def filter_list_for_esrb_rating(games_list, esrb_rating):
    return [videogame for videogame in games_list if videogame["esrb_rating"] == esrb_rating]

def main():
    esrb_input = input("Ingrese la clasificación ESRB o 0 para salir: ")
    file_path = os.path.join(os.path.dirname(__file__),"Videojuegos.csv")
    if esrb_input != "0":
        videojuegos = read_csv_file(file_path)
        filtered_videogames = filter_list_for_esrb_rating(videojuegos, esrb_input)
        print_videogames(filtered_videogames)

if __name__ == "__main__":
    main()
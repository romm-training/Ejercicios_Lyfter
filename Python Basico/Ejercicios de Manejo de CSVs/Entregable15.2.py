import os, csv

DEFAULT_ENCODING = "utf-8"

def input_flow_control():
    local_flow_control = 1
    flow_control = 1
    while local_flow_control == 1:
        try:
            flow_control = int(input("Desea continuar? 1-SI 0-NO: "))
            if flow_control != 0 and flow_control != 1:
                raise ValueError()
            local_flow_control = 0
        except ValueError:
            print("La opción ingresada es incorrecta. El programa continua.")
            continue

    return flow_control

def append_to_csv_file(file_path, data, headers):
    with open(file_path, "a", encoding=DEFAULT_ENCODING, newline="") as file:
        writer = csv.DictWriter(file, headers, delimiter="\t")
        writer.writeheader()
        writer.writerows(data)

def main():
    file_path = os.path.join(os.path.dirname(__file__),"Entregable15_2.csv")
    flow_controller = 1
    videogames = []

    while flow_controller == 1:
        videogame = {}
        print("Información del videojuego")
        videogame["title"] = input("Título: ")
        videogame["genre"] = input("Genero: ")
        videogame["developer"] = input("Desarrollador: ")
        videogame["esrb_rating"] = input("Clasificación ESRB: ")

        videogames.append(videogame)

        flow_controller = input_flow_control()

    append_to_csv_file(file_path, videogames, videogames[0].keys())

if __name__ == "__main__":
    main()
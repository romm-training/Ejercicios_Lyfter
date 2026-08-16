import FreeSimpleGUI as sg

counter = 0

layout = [
    [sg.Text("Haz clic en lo que quieras hacer")],
    # Se usa la key "-COUNTER-" para identificar este elemento
    [sg.Text(counter, key="-COUNTER-")],
    [sg.Button("Sumar"), sg.Button("Restar")],
]

window = sg.Window("Primer programa", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "Sumar":
        counter += 1
    elif event == "Restar":
        counter -= 1

    window["-COUNTER-"].update(counter)

window.close()
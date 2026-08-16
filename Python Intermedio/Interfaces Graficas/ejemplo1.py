import FreeSimpleGUI as sg

layout = [
    [sg.Text("Bienvenido a la aplicacion")],
    [sg.Button("Continuar")]
]

# Se crea la ventana basada en nuestro plano (layout)
windows = sg.Window("Mi primera aplicacion", layout)

# Se inicia el Event Loop
while True:
    # El programa se "detiene" aqui (bloqueo) esperando una accion
    event, values = windows.read()

    # Si el usuario cierra la ventana, se interrumpe el ciclo
    if event == sg.WIN_CLOSED:
        break

    # Si ocurre el event de pulsar "Continuar"
    if event == "Continuar":
        print("Continuar")

windows.close()
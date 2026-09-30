class HTTP_CODES():
    R200 = "200"
    R201 = "201"
    R202 = "202"
    R204 = "204"
    E400 = "400"
    E404 = "404"
    E500 = "500"

    def __setattr__(self, name, value):
        raise AttributeError(f"No se puede modificar la constante '{name}'")
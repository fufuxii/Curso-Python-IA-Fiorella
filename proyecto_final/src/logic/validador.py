from src.api.rae import consultar_palabra
from src.logic.texto import quitar_tildes


def validar_palabra(palabra, letras, letra_central):
    palabra = palabra.strip().lower()

    if len(palabra) < 3:
        return False

    letras = {quitar_tildes(l.lower()) for l in letras}
    letra_central = quitar_tildes(letra_central.lower())
    base = quitar_tildes(palabra)

    if letra_central not in base:
        return False

    if not all(l in letras for l in base):
        return False

    return consultar_palabra(palabra)

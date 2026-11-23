from proyecto_final.src.api.rae import consultar_palabra


def validar_palabra(palabra, letras, letra_central):

    palabra = palabra.strip().lower()
    letras = {letra.lower() for letra in letras}
    letra_central = letra_central.lower()

    if not palabra:
        return False

    if len(palabra) < 3:
        return False

    if letra_central not in palabra:
        return False

    if not all(letra in letras for letra in palabra):
        return False

    return consultar_palabra(palabra)

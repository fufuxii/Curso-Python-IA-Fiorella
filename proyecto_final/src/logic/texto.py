import unicodedata


def quitar_tildes(texto: str) -> str:
    """Quita tildes pero conserva la ñ."""
    
    texto = texto.replace("ñ", "\0").replace("Ñ", "\1")
    nfd = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return sin_tildes.replace("\0", "ñ").replace("\1", "Ñ")
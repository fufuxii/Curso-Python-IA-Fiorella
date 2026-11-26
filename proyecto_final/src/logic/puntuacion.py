
def puntos_palabra(palabra: str) -> int:
    """
    Calcula los puntos de una palabra. Cada carácter equivale a un punto.
    """
    
    return len(palabra)


def puntos_totales(palabras_encontradas: list[str]) -> int:
    """
    Calcula la puntuación total de la partida.
    """
    
    return sum(puntos_palabra(palabra) for palabra in palabras_encontradas)

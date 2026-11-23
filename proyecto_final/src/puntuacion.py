"""Puntos y rangos."""

RANGOS = [
    (0, "Principiante"),
    (10, "Aprendiz"),
    (25, "Buen ritmo"),
    (40, "Sólido"),
    (60, "Experto"),
    (80, "Genio"),
    (100, "¡Todas las palabras!"),
]


def puntos_palabra(palabra_norm: str, tablero, config: dict) -> int:
    """3-4 letras = 1 punto; más largas = 1 punto por letra; pangrama = + bonus."""
    n = len(palabra_norm)
    puntos = 1 if n <= 4 else n
    if palabra_norm in tablero.pangramas:
        puntos += config["puntos_pangrama"]
    return puntos


def puntos_totales(encontradas, tablero, config: dict) -> int:
    return sum(puntos_palabra(p, tablero, config) for p in encontradas)


def puntos_maximos(tablero, config: dict) -> int:
    return puntos_totales(tablero.palabras, tablero, config)


def rango(puntos: int, maximo: int) -> str:
    pct = 100 * puntos / maximo if maximo else 0
    actual = RANGOS[0][1]
    for minimo, nombre in RANGOS:
        if pct >= minimo:
            actual = nombre
    return actual
import json
import random

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Tablero:
    central: str
    externas: list[str]

    @property
    def letras(self) -> set[str]:
        return set(self.externas) | {self.central}


def cargar_palabras_base():
    ruta = Path(__file__).resolve().parents[2] / "data" / "palabras.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return [
        palabra.upper()
        for palabra in datos["palabras_base"]
        if len(palabra) == 7 and len(set(palabra.upper())) == 7
    ]


def generar_tablero(semilla=None) -> Tablero:

    rng = random.Random(semilla)

    palabras = cargar_palabras_base()

    if not palabras:
        raise ValueError("No hay palabras válidas para generar tableros.")

    palabra = rng.choice(palabras)

    letras = list(palabra)

    central = rng.choice(letras)

    externas = [
        letra for letra in letras
        if letra != central
    ]

    rng.shuffle(externas)

    return Tablero(
        central=central,
        externas=externas
    )
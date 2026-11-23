"""Generación del tablero (letra central + letras externas + palabras válidas)."""
import random
from dataclasses import dataclass, field


@dataclass
class Tablero:
    central: str
    externas: list[str]
    palabras: dict[str, str]
    pangramas: set[str] = field(default_factory=set)

    @property
    def letras(self) -> set[str]:
        return set(self.externas) | {self.central}

    def mezclar(self, rng: random.Random | None = None) -> None:
        (rng or random).shuffle(self.externas)


def _palabras_validas(diccionario, letras, central, longitud_minima):
    return {
        norm: orig for norm, orig in diccionario.items()
        if len(norm) >= longitud_minima and central in norm and set(norm) <= letras
    }


def generar_tablero(diccionario: dict[str, str], config: dict,
                    semilla: int | None = None) -> Tablero:
    """Elige un pangrama, una letra central y calcula todas las palabras válidas."""
    
    rng = random.Random(semilla)
    n = config["letras_totales"]
    minimo = config["longitud_minima"]
    min_palabras = config["minimo_palabras_por_tablero"]

    candidatos = sorted(p for p in diccionario if len(set(p)) == n)
    rng.shuffle(candidatos)

    for pangrama in candidatos:
        letras = set(pangrama)
        centros = sorted(letras)
        rng.shuffle(centros)
        
        for central in centros:
            validas = _palabras_validas(diccionario, letras, central, minimo)
            
            if len(validas) >= min_palabras:
                externas = sorted(letras - {central})
                rng.shuffle(externas)
                pangramas = {p for p in validas if set(p) == letras}
                return Tablero(central, externas, validas, pangramas)

    raise ValueError(
        "No se pudo generar un tablero: faltan pangramas o palabras en el JSON."
    )
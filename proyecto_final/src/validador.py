import json
import unicodedata
from pathlib import Path
from typing import NamedTuple

CONFIG_POR_DEFECTO = {
    "letras_totales": 7,
    "longitud_minima": 3,
    "minimo_palabras_por_tablero": 10,
    "tiempo_segundos": 180,
    "puntos_pangrama": 7,
}


class Resultado(NamedTuple):
    valida: bool
    mensaje: str


def normalizar(texto: str) -> str:
    """Pone el texto en mayúsculas y sin tildes/diéresis, pero conservando la Ñ."""
    
    texto = texto.strip().upper().replace("Ñ", "\0")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.replace("\0", "Ñ")


def cargar_datos(ruta) -> tuple[dict, dict[str, str]]:
    """Lee el JSON. Devuelve (config, diccionario) donde el diccionario
    es {palabra_normalizada: palabra_original_para_mostrar}."""
    
    with open(Path(ruta), encoding="utf-8") as f:
        datos = json.load(f)

    config = {**CONFIG_POR_DEFECTO, **datos.get("config", {})}
    
    diccionario: dict[str, str] = {}
    
    for original in datos.get("palabras", []):
        norm = normalizar(original)
        
        if norm.isalpha() and norm not in diccionario:
            diccionario[norm] = original.strip().lower()
    
    return config, diccionario


def validar_palabra(entrada: str, tablero, encontradas: set[str],
                    longitud_minima: int) -> Resultado:
    """Comprueba una palabra."""
    
    palabra = normalizar(entrada)
    
    if not palabra:
        return Resultado(False, "Escribe una palabra.")
    
    if len(palabra) < longitud_minima:
        return Resultado(False, f"Muy corta (mínimo {longitud_minima} letras).")
    
    if not set(palabra) <= tablero.letras:
        return Resultado(False, "Usa solo las letras del tablero.")
    
    if tablero.central not in palabra:
        return Resultado(False, f"Debe contener la letra central ({tablero.central}).")
    
    if palabra in encontradas:
        return Resultado(False, "Ya la encontraste.")
    
    if palabra not in tablero.palabras:
        return Resultado(False, "No está en el diccionario.")
    
    return Resultado(True, "¡Correcto!")
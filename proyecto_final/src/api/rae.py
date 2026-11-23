import os
import requests

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://rae-api.com/api/words"
API_KEY = os.getenv("RAE_API_KEY")

_cache: dict[str, bool] = {}


def consultar_palabra(palabra):
    palabra = palabra.lower()

    if palabra in _cache:
        return _cache[palabra]

    try:
        respuesta = requests.get(
            f"{BASE_URL}/{palabra}",
            headers={"X-API-Key": API_KEY},
            timeout=5,
        )

        if respuesta.status_code == 404:
            _cache[palabra] = False
            return False

        respuesta.raise_for_status()
        existe = bool(respuesta.json().get("ok", False))
        _cache[palabra] = existe  
        
        return existe

    except requests.RequestException as error:
        print(f"Error al consultar la RAE: {error}")
        return False 
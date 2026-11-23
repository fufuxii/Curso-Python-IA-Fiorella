import requests
import os

from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

BASE_URL = "https://rae-api.com/api/words"
API_KEY = os.getenv("RAE_API_KEY")


@lru_cache(maxsize=1000)
def consultar_palabra(palabra):

    url = f"{BASE_URL}/{palabra.lower()}"

    headers = {
        "X-API-Key": API_KEY
    }

    try:
        respuesta = requests.get(
            url,
            headers=headers,
            timeout=5
        )

        if respuesta.status_code == 404:
            return False

        respuesta.raise_for_status()

        datos = respuesta.json()

        return datos.get("ok", False)

    except requests.RequestException as error:
        print(f"Error al consultar la RAE: {error}")
        return False
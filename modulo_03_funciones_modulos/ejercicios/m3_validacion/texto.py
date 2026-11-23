"""Validación y normalización de textos."""

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"


def esta_vacio(texto: str | None) -> bool:
    """Indica si el texto es ``None``, está vacío o solo contiene espacios.

    >>> esta_vacio("   ")
    True
    >>> esta_vacio(" a ")
    False
    """
    return texto is None or texto.strip() == ""


def normalizar_nombre(nombre: str) -> str:
    """Quita los espacios sobrantes y pone en mayúscula la inicial de cada palabra.

    >>> normalizar_nombre("  ada   LOVELACE ")
    'Ada Lovelace'
    """
    return " ".join(nombre.split()).title()


def es_email(texto: str) -> bool:
    """Comprueba de forma sencilla que el texto tiene forma de correo.

    Reglas: no contiene espacios, tiene exactamente una arroba, hay texto
    antes de la arroba, y el dominio contiene al menos un punto que no está
    ni al principio ni al final.

    >>> es_email("ada@ejemplo.com")
    True
    >>> es_email("ada@ejemplo")
    False
    """
    if texto.count("@") != 1 or any(caracter.isspace() for caracter in texto):
        return False

    local, dominio = texto.split("@")
    
    if not local or "." not in dominio:
        return False

    return not dominio.startswith(".") and not dominio.endswith(".")


def es_dni(texto: str) -> bool:
    """Comprueba que el texto es un DNI válido: ocho dígitos y la letra correcta.

    La letra se obtiene tomando el resto de dividir el número entre 23 y
    usándolo como posición en ``LETRAS_DNI``. Admite la letra en minúscula y
    espacios alrededor.

    >>> es_dni("12345678Z")
    True
    >>> es_dni("12345678A")
    False
    """
    dni = texto.strip()
    
    if len(dni) != 9 or not dni[:8].isdigit() or not dni[8].isalpha():
        return False

    numero = int(dni[:8])
    
    return dni[8].upper() == LETRAS_DNI[numero % 23]

"""Módulo 2 - Ejercicio 2: operadores."""


def es_bisiesto(anio: int) -> bool:
    """Indica si un año es bisiesto.

    Es bisiesto si es divisible entre 4, salvo los divisibles entre 100 que
    no lo sean también entre 400.

    >>> es_bisiesto(2024), es_bisiesto(1900), es_bisiesto(2000)
    (True, False, True)
    """
    if ((anio % 4 == 0) and (anio % 100 != 0 or anio % 400 == 0)):
        return True
    else:
        return False


def segundos_a_hms(segundos: int) -> str:
    """Convierte segundos al formato HH:MM:SS.

    >>> segundos_a_hms(3725)
    '01:02:05'
    """
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
    

def nombre_o_anonimo(nombre: str | None) -> str:
    """Devuelve el nombre sin espacios sobrantes o "Anónimo" si no hay.

    >>> nombre_o_anonimo("  Ada "), nombre_o_anonimo(""), nombre_o_anonimo(None)
    ('Ada', 'Anónimo', 'Anónimo')
    """
    if nombre is None: 
        return "Anónimo"
    nombre_limpio = nombre.strip()
    if nombre_limpio == "":
        return "Anónimo"
    else:
        return nombre_limpio
        

def en_rango(valor: float, minimo: float, maximo: float) -> bool:
    """Indica si ``valor`` está entre ``minimo`` y ``maximo``, ambos incluidos.

    >>> en_rango(5, 1, 10), en_rango(11, 1, 10)
    (True, False)
    """
    if (valor >= minimo and valor <= maximo):
        return True
    else:
        return False


def es_par(numero: int) -> bool:
    """Indica si un entero es par, también si es negativo.

    >>> es_par(-4), es_par(7)
    (True, False)
    """
    if (numero % 2 == 0):
        return True
    else:
        return False


def reparto(total: int, personas: int) -> tuple[int, int]:
    """Reparte ``total`` unidades entre ``personas``.

    Devuelve cuántas tocan a cada una y cuántas sobran.

    >>> reparto(17, 5)
    (3, 2)
    """
    toca = int(total / personas)
    sobra = total - (toca * personas)
    return (toca, sobra)

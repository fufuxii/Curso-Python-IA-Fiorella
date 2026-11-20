"""Módulo 2 - Ejercicio 4: bucles."""


import math

def factorial(n: int) -> int:
    """Devuelve el factorial de ``n`` (n >= 0) usando un bucle.

    >>> factorial(5), factorial(0)
    (120, 1)
    """
    return math.factorial(n)


def es_primo(n: int) -> bool:
    """Indica si ``n`` es un número primo.

    >>> es_primo(13), es_primo(15), es_primo(1)
    (True, False, False)
    """
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def invertir(texto: str) -> str:
    """Devuelve ``texto`` del revés usando un bucle.

    >>> invertir("Python")
    'nohtyP'
    """
    texto_reves = []
    for c in reversed(texto):
        texto_reves.append(c)
    return "".join(texto_reves)


def contar_vocales(texto: str) -> int:
    """Cuenta las vocales de ``texto``, sin distinguir mayúsculas ni tildes.

    >>> contar_vocales("Programación")
    5
    """
    num_vocales = 0
    for c in texto:
        if c.lower() in "aeiouáéíóúü":
            num_vocales += 1
    return num_vocales


def suma_digitos(numero: int) -> int:
    """Suma los dígitos de un entero, ignorando el signo. Usa un while.

    >>> suma_digitos(1234), suma_digitos(-905)
    (10, 14)
    """
    cadena = str(abs(numero))
    suma = 0

    for i in range(len(cadena)):
        suma += int(cadena[i])
        i += 1
        
    return suma


def fizzbuzz(n: int) -> str:
    """Devuelve la secuencia FizzBuzz de 1 a ``n`` separada por espacios.

    Los múltiplos de 3 se sustituyen por "Fizz", los de 5 por "Buzz" y los de
    ambos por "FizzBuzz".

    >>> fizzbuzz(5)
    '1 2 Fizz 4 Buzz'
    """
    secuencia = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            secuencia.append("FizzBuzz")
        elif i % 3 == 0:
            secuencia.append("Fizz")
        elif i % 5 == 0:
            secuencia.append("Buzz")
        else:
            secuencia.append(str(i))

    return " ".join(secuencia)


def tabla_multiplicar(numero: int) -> str:
    """Devuelve la tabla de multiplicar del 1 al 10, una línea por producto.

    >>> print(tabla_multiplicar(7).splitlines()[2])
    7 x  3 =  21
    """
    lineas = []

    for i in range(1, 11):
        producto = numero * i
        lineas.append(f"{numero} x {i:2d} = {producto:3d}")

    return "\n".join(lineas)


def primer_multiplo_comun(a: int, b: int) -> int:
    """Devuelve el mínimo común múltiplo de dos enteros positivos con un while.

    >>> primer_multiplo_comun(4, 6)
    12
    """
    num_a = a
    num_b = b

    while b:
        a, b = b, a % b

    mcd = abs(a)

    return abs(num_a * num_b) // mcd

"""Módulo 1 - Ejercicio 2: operaciones con dos números."""


def sumar(a, b):
    """Devuelve a + b."""
    return a + b


def restar(a, b):
    """Devuelve a - b."""
    return a - b


def multiplicar(a, b):
    """Devuelve a * b."""
    return a * b


def dividir(a, b):
    """Devuelve la división real de a entre b (siempre un float)."""
    return a / b


def division_entera(a, b):
    """Devuelve el cociente entero de a entre b."""
    return a // b


def resto(a, b):
    """Devuelve el resto de dividir a entre b."""
    return a % b


def potencia(a, b):
    """Devuelve a elevado a b."""
    return a ** b


def resumen(a, b):
    """Devuelve todas las operaciones en una sola cadena.

    >>> resumen(7, 2)
    '7 + 2 = 9 | 7 - 2 = 5 | 7 * 2 = 14 | 7 / 2 = 3.50 | 7 // 2 = 3 | 7 % 2 = 1 | 7 ** 2 = 49'
    """
    suma = f"{a} + {b} = {sumar(a, b)}"
    resta = f"{a} - {b} = {restar(a, b)}"
    mult = f"{a} * {b} = {multiplicar(a, b)}"
    div = f"{a} / {b} = {dividir(a, b):.2f}"
    div_entera = f"{a} // {b} = {division_entera(a, b)}"
    div_resto = f"{a} % {b} = {resto(a, b)}"
    pot = f"{a} ** {b} = {potencia(a, b)}"
    return f"{suma} | {resta} | {mult} | {div} | {div_entera} | {div_resto} | {pot}"

def main():
    """Pide dos números enteros por teclado e imprime el resumen."""
    a = int(input("Primer número: "))
    b = int(input("Segundo número: "))
    print(resumen(a, b))


if __name__ == "__main__":
    main()

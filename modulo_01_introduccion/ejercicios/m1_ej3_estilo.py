"""Módulo 1 - Ejercicio 3: código con estilo.

La función de abajo funciona, pero ignora PEP 8. Reescríbela siguiendo las
indicaciones del enunciado sin cambiar su comportamiento.
"""

IVA_GENERAL = 21

def precio_final(precio, iva = IVA_GENERAL, descuento = 0):
    """
    Calcular el precio final según un precio, el IVA de un 21%,
    y un descuento (si no se especifica es un 0).
    """
    x = precio - precio * descuento / 100
    y = x + x * iva / 100
    return round(y, 2)

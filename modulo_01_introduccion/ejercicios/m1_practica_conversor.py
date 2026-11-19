"""Módulo 1 - Práctica 1: conversor de unidades.

Lee el enunciado en PRACTICA_1.md.
"""

# 1. Define aquí las constantes KM_POR_MILLA y KG_POR_LIBRA
KM_POR_MILLA = 1.609344
KG_POR_LIBRA = 0.45359237


def celsius_a_fahrenheit(grados):
    """Convierte grados Celsius a Fahrenheit."""
    return(grados * 9 / 5 + 32)


def fahrenheit_a_celsius(grados):
    """Convierte grados Fahrenheit a Celsius."""
    return((grados - 32)*(5 / 9))


def km_a_millas(km):
    """Convierte kilómetros a millas."""
    return(km / KM_POR_MILLA)


def millas_a_km(millas):
    """Convierte millas a kilómetros."""
    return(millas * KM_POR_MILLA)


def kg_a_libras(kg):
    """Convierte kilogramos a libras."""
    return(kg / KG_POR_LIBRA)


def libras_a_kg(libras):
    """Convierte libras a kilogramos."""
    return(libras * KG_POR_LIBRA)


def formatear(valor, unidad_origen, resultado, unidad_destino):
    """Devuelve el texto de la conversión con dos decimales.

    >>> formatear(100, "°C", 212.0, "°F")
    '100.00 °C = 212.00 °F'
    """

    return f"{valor:.2f} {unidad_origen} = {resultado:.2f} {unidad_destino}"


def main():
    """Muestra el menú, pide los datos e imprime el resultado."""

    opcion = input(
        "Conversor de unidades\n"
        "1. Celsius a Fahrenheit\n"
        "2. Fahrenheit a Celsius\n"
        "3. Kilómetros a millas\n"
        "4. Millas a kilómetros\n"
        "5. Kilogramos a libras\n"
        "6. Libras a kilogramos\n"
        "Elige una opción (1-6): "
    )

    match opcion:
        case "1":
            funcion = celsius_a_fahrenheit
            unidad_origen, unidad_destino = "°C", "°F"
        case "2":
            funcion = fahrenheit_a_celsius
            unidad_origen, unidad_destino = "°F", "°C"
        case "3":
            funcion = km_a_millas
            unidad_origen, unidad_destino = "km", "mi"
        case "4":
            funcion = millas_a_km
            unidad_origen, unidad_destino = "mi", "km"
        case "5":
            funcion = kg_a_libras
            unidad_origen, unidad_destino = "kg", "lb"
        case "6":
            funcion = libras_a_kg
            unidad_origen, unidad_destino = "lb", "kg"
        case _:
            print("Opción no válida")
            return

    valor = float(input("Valor a convertir: "))
    resultado = funcion(valor)
    print(formatear(valor, unidad_origen, resultado, unidad_destino))


if __name__ == "__main__":
    main()

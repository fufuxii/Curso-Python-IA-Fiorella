"""Módulo 2 - Práctica 2, parte B: calculadora de nómina."""


SEGURIDAD_SOCIAL = 6.35
PAGAS = 12


def calcular_irpf(bruto_anual: float) -> float:
    """Calcula la retención anual de IRPF con una escala progresiva.

    Cada tramo se aplica solo a la parte del salario que cae dentro de él.

    >>> calcular_irpf(30000)
    7165.5
    """
    if bruto_anual <= 12450:
        irpf = bruto_anual * 0.19

    elif bruto_anual <= 20200:
        irpf = (12450 * 0.19) + ((bruto_anual - 12450) * 0.24)

    elif bruto_anual <= 35200:
        irpf = (12450 * 0.19) + (7750 * 0.24) + ((bruto_anual - 20200) * 0.30)

    elif bruto_anual <= 60000:
        irpf = (12450 * 0.19) + (7750 * 0.24) + (15000 * 0.30) + ((bruto_anual - 35200) * 0.37)

    else:
        irpf = (12450 * 0.19) + (7750 * 0.24) + (15000 * 0.30) + (24800 * 0.37) + ((bruto_anual - 60000) * 0.45)

    return round(irpf, 2)


def calcular_seguridad_social(bruto_anual: float) -> float:
    """Calcula la cotización anual del trabajador a la Seguridad Social.

    >>> calcular_seguridad_social(30000)
    1905.0
    """
    return round(bruto_anual * SEGURIDAD_SOCIAL / 100, 2)


def calcular_neto_anual(bruto_anual: float) -> float:
    """Devuelve el salario neto anual: bruto menos IRPF y Seguridad Social.

    >>> calcular_neto_anual(30000)
    20929.5
    """
    irpf = calcular_irpf(bruto_anual)
    seguridad_social = calcular_seguridad_social(bruto_anual)
    return round(bruto_anual - irpf - seguridad_social, 2)


def tipo_efectivo(bruto_anual: float) -> float:
    """Devuelve el porcentaje de IRPF sobre el bruto, con dos decimales.

    Si el bruto es cero o negativo devuelve 0.0.

    >>> tipo_efectivo(30000)
    23.89
    """
    if bruto_anual <= 0:
        return 0.0

    irpf = calcular_irpf(bruto_anual)

    return round((irpf / bruto_anual) * 100, 2)


def formatear_nomina(bruto_anual: float) -> str:
    """Devuelve el resumen de la nómina en cinco líneas alineadas.

    >>> print(formatear_nomina(30000))
    Bruto anual            30,000.00
    IRPF (23.89 %)         -7,165.50
    Seguridad Social       -1,905.00
    Neto anual             20,929.50
    Neto mensual            1,744.12
    """
    irpf = calcular_irpf(bruto_anual)
    seguridad_social = calcular_seguridad_social(bruto_anual)
    neto = calcular_neto_anual(bruto_anual)
    porcentaje = tipo_efectivo(bruto_anual)
    neto_mensual = round(neto / PAGAS, 2)

    etiqueta_irpf = f"IRPF ({porcentaje:.2f} %)"

    resumen = (
        f"{'Bruto anual':<20}{bruto_anual:>12,.2f}\n"
        f"{etiqueta_irpf:<20}{-irpf:>12,.2f}\n"
        f"{'Seguridad Social':<20}{-seguridad_social:>12,.2f}\n"
        f"{'Neto anual':<20}{neto:>12,.2f}\n"
        f"{'Neto mensual':<20}{neto_mensual:>12,.2f}"
    )

    return resumen


def main() -> None:
    """Pide el salario bruto anual y muestra la nómina."""

    texto = input("Introduce el salario bruto anual: ")

    if not texto.replace(".", "", 1).isdigit():
        print("Importe no válido")
        return

    bruto_anual = float(texto)

    if bruto_anual <= 0:
        print("Importe no válido")
        return

    print(formatear_nomina(bruto_anual))


if __name__ == "__main__":
    main()

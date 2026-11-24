"""Módulo 4 - Práctica 4: análisis de ventas en memoria.

Cada venta es un diccionario con las claves "fecha", "vendedor", "region",
"producto", "categoria", "unidades" y "precio". Ninguna función modifica la
lista de ventas que recibe.
"""

from m4_datos_ventas import VENTAS

ANCHO = 44


def importe(venta: dict) -> float:
    """Devuelve el importe de una venta: unidades por precio, con dos decimales.

    >>> importe({"unidades": 3, "precio": 19.9})
    59.7
    """
    return round(venta["unidades"] * venta["precio"], 2)


def total_ventas(ventas: list[dict]) -> float:
    """Devuelve la suma de los importes de todas las ventas, con dos decimales."""
    return round(sum(importe(venta) for venta in ventas), 2)


def filtrar_ventas(ventas: list[dict], *, region: str | None = None,
                   categoria: str | None = None, vendedor: str | None = None,
                   desde: str | None = None, hasta: str | None = None) -> list[dict]:
    """Devuelve las ventas que cumplen todos los criterios indicados.

    Un criterio que vale ``None`` no se aplica. ``desde`` y ``hasta`` son
    fechas ISO y las dos están incluidas en el intervalo.
    """
    return [
        venta
        for venta in ventas
        if (region is None or venta["region"] == region)
        and (categoria is None or venta["categoria"] == categoria)
        and (vendedor is None or venta["vendedor"] == vendedor)
        and (desde is None or venta["fecha"] >= desde)
        and (hasta is None or venta["fecha"] <= hasta)
    ]


def importe_por(ventas: list[dict], campo: str) -> dict[str, float]:
    """Agrupa las ventas por ``campo`` y devuelve el importe total de cada grupo.

    Los importes van redondeados a dos decimales.

    >>> importe_por([{"region": "Norte", "unidades": 2, "precio": 10.0}], "region")
    {'Norte': 20.0}
    """
    importes = {}
    for venta in ventas:
        clave = venta[campo]
        importes[clave] = importes.get(clave, 0.0) + importe(venta)
    return {clave: round(total, 2) for clave, total in importes.items()}


def unidades_por_producto(ventas: list[dict]) -> dict[str, int]:
    """Devuelve las unidades totales vendidas de cada producto."""
    unidades = {}
    for venta in ventas:
        producto = venta["producto"]
        unidades[producto] = unidades.get(producto, 0) + venta["unidades"]
    return unidades


def ranking(ventas: list[dict], campo: str, cantidad: int = 3) -> list[tuple[str, float]]:
    """Devuelve los ``cantidad`` grupos con mayor importe, como tuplas (clave, importe).

    De mayor a menor importe. A igual importe, por orden alfabético de la clave.
    """
    grupos = importe_por(ventas, campo)
    return sorted(grupos.items(), key=lambda grupo: (-grupo[1], grupo[0]))[:cantidad]


def producto_mas_vendido(ventas: list[dict]) -> str | None:
    """Devuelve el producto con más unidades vendidas, o ``None`` si no hay ventas.

    En caso de empate, el primero por orden alfabético.
    """
    unidades = unidades_por_producto(ventas)
    if not unidades:
        return None
    return min(unidades.items(), key=lambda grupo: (-grupo[1], grupo[0]))[0]


def ticket_medio(ventas: list[dict]) -> float:
    """Devuelve el importe medio por venta, con dos decimales. Sin ventas, 0.0."""
    if not ventas:
        return 0.0
    return round(total_ventas(ventas) / len(ventas), 2)


def generar_informe(ventas: list[dict]) -> str:
    """Devuelve el informe de ventas como texto, con el formato del enunciado."""
    producto = producto_mas_vendido(ventas)
    lineas = [
        "=" * ANCHO,
        "INFORME DE VENTAS".center(ANCHO),
        "=" * ANCHO,
        f"{'Ventas registradas':<30}{len(ventas):>14}",
        f"{'Importe total':<30}{total_ventas(ventas):>14,.2f}",
        f"{'Ticket medio':<30}{ticket_medio(ventas):>14,.2f}",
        f"{'Producto más vendido':<30}{(producto if producto is not None else '-'):>14}",
    ]

    for titulo, campo in (
        ("Por región", "region"),
        ("Por categoría", "categoria"),
        ("Por vendedor", "vendedor"),
    ):
        lineas.append("-" * ANCHO)
        lineas.append(titulo)
        lineas.extend(
            f"  {clave:<28}{importe_grupo:>14,.2f}"
            for clave, importe_grupo in ranking(ventas, campo, len(ventas))
        )

    lineas.append("=" * ANCHO)
    return "\n".join(lineas)


def main():
    print(generar_informe(VENTAS))
    print()
    print("Solo la región Sur, segunda quincena:")
    print(generar_informe(filtrar_ventas(VENTAS, region="Sur", desde="2026-10-16")))


if __name__ == "__main__":
    main()

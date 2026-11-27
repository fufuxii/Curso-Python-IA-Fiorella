"""Módulo 7 - Ejercicio 5: visualización con Matplotlib.

Las funciones crean la figura y la devuelven. No llaman a ``plt.show()``: quien
las usa decide si la muestra, la guarda o la prueba.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def grafico_barras(serie: pd.Series, titulo: str, etiqueta_y: str = "Importe (€)") -> Figure:
    """Devuelve una figura con un gráfico de barras: una barra por elemento de la serie.

    El eje X muestra el índice de la serie. La figura lleva el título y la
    etiqueta del eje Y indicados.
    """
    figura, eje = plt.subplots()
    eje.bar(serie.index, serie.values)
    eje.set_title(titulo)
    eje.set_ylabel(etiqueta_y)
    return figura


def grafico_lineas(serie: pd.Series, titulo: str, etiqueta_y: str = "Importe (€)") -> Figure:
    """Devuelve una figura con un gráfico de líneas con un marcador en cada punto.

    Pensado para la evolución mensual: el índice de la serie va en el eje X.
    La figura lleva título, etiqueta del eje Y y rejilla.
    """
    figura, eje = plt.subplots()
    eje.plot(serie.index, serie.values, marker="o")
    eje.set_title(titulo)
    eje.set_ylabel(etiqueta_y)
    eje.grid(True)
    return figura


def histograma(valores, titulo: str, intervalos: int = 10) -> Figure:
    """Devuelve una figura con el histograma de los valores, con ``intervalos`` barras."""
    figura, eje = plt.subplots()
    eje.hist(valores, bins=intervalos)
    eje.set_title(titulo)
    return figura


def panel(por_vendedor: pd.Series, mensual: pd.Series, titulo: str) -> Figure:
    """Devuelve una figura con dos gráficos, uno al lado del otro.

    A la izquierda, barras con el importe por vendedor, con el título
    "Por vendedor". A la derecha, líneas con la evolución mensual, con el
    título "Evolución mensual". ``titulo`` es el título general de la figura.
    """
    figura, (izquierda, derecha) = plt.subplots(1, 2)
    izquierda.bar(por_vendedor.index, por_vendedor.values)
    izquierda.set_title("Por vendedor")
    derecha.plot(mensual.index, mensual.values, marker="o")
    derecha.set_title("Evolución mensual")
    derecha.grid(True)
    figura.suptitle(titulo)
    return figura


def guardar(figura: Figure, ruta: str | Path) -> Path:
    """Guarda la figura en ``ruta`` como PNG a 150 ppp, cierra la figura y devuelve la ruta.

    Crea la carpeta de destino si no existe.
    """
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(ruta, format="png", dpi=150)
    plt.close(figura)
    return ruta

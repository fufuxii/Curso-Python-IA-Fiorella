from pathlib import Path

import pytest

from src.generador import Tablero, generar_tablero
from src.puntuacion import puntos_maximos, puntos_palabra, puntos_totales, rango
from src.temporizador import Temporizador
from src.validador import cargar_datos, normalizar, validar_palabra

RUTA = Path(__file__).parent.parent / "data" / "palabras.json"


@pytest.fixture
def datos():
    return cargar_datos(RUTA)


@pytest.fixture
def tablero(datos):
    config, dic = datos
    return generar_tablero(dic, config, semilla=1)


# ---------- normalizar ----------
def test_normalizar_quita_tildes_y_conserva_enie():
    assert normalizar(" Canción ") == "CANCION"
    assert normalizar("caña") == "CAÑA"


# ---------- generador ----------
def test_tablero_tiene_7_letras_y_pangrama(tablero):
    assert len(tablero.letras) == 7
    assert tablero.pangramas


def test_todas_las_palabras_cumplen_reglas(tablero):
    for p in tablero.palabras:
        assert tablero.central in p
        assert set(p) <= tablero.letras
        assert len(p) >= 3


def test_misma_semilla_mismo_tablero(datos):
    config, dic = datos
    a = generar_tablero(dic, config, semilla=5)
    b = generar_tablero(dic, config, semilla=5)
    assert (a.central, a.externas) == (b.central, b.externas)


def test_error_si_no_hay_pangramas():
    with pytest.raises(ValueError):
        generar_tablero({"CASA": "casa"}, {"letras_totales": 7, "longitud_minima": 3,
                                           "minimo_palabras_por_tablero": 1})


# ---------- validador ----------
def test_validaciones(tablero):
    palabra_ok = sorted(tablero.palabras)[0]
    assert validar_palabra(palabra_ok, tablero, set(), 3).valida
    assert not validar_palabra(palabra_ok, tablero, {palabra_ok}, 3).valida   # repetida
    assert not validar_palabra("ab", tablero, set(), 3).valida                # corta
    assert not validar_palabra("PERRO", tablero, set(), 3).valida             # letras ajenas
    assert not validar_palabra("", tablero, set(), 3).valida


def test_exige_letra_central():
    t = Tablero("A", list("BCDEFG"), {"BEBE": "bebe"})
    r = validar_palabra("bebe", t, set(), 3)
    assert not r.valida and "central" in r.mensaje


def test_acepta_entrada_con_tilde():
    t = Tablero("O", list("CANIST"), {"CANCION": "canción"}, set())
    assert validar_palabra("Canción", t, set(), 3).valida


# ---------- puntuación ----------
def test_puntos(tablero, datos):
    config, _ = datos
    pang = next(iter(tablero.pangramas))
    assert puntos_palabra(pang, tablero, config) == len(pang) + config["puntos_pangrama"]
    assert puntos_totales(tablero.palabras, tablero, config) == puntos_maximos(tablero, config)


def test_rangos():
    assert rango(0, 100) == "Principiante"
    assert rango(100, 100) == "¡Todas las palabras!"


# ---------- temporizador ----------
def test_temporizador():
    t = [0.0]
    cron = Temporizador(60, reloj=lambda: t[0])
    assert not cron.terminado and cron.formateado() == "1:00"
    cron.iniciar()
    t[0] = 15
    assert cron.restante() == 45 and not cron.terminado
    t[0] = 61
    assert cron.restante() == 0 and cron.terminado
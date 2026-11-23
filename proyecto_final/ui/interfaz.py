import math
from pathlib import Path

import streamlit as st

from src.generador import generar_tablero
from src.puntuacion import puntos_maximos, puntos_palabra, puntos_totales, rango
from src.temporizador import Temporizador
from src.validador import cargar_datos, normalizar, validar_palabra

RUTA_JSON = Path(__file__).resolve().parent.parent / "data" / "palabras.json"

CSS = """
<style>
.panal { position: relative; width: 300px; height: 280px; margin: 0 auto 8px auto; }
.hex { position: absolute; width: 84px; height: 73px;
       clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
       display: flex; align-items: center; justify-content: center;
       font: 700 28px sans-serif; background: #e3e3e3; color: #222; }
.hex.central { background: #f7c600; }
.pangrama { font-weight: 700; }
</style>
"""


# ---------------------------------------------------------------- estado
@st.cache_data
def _cargar(ruta: str):
    return cargar_datos(ruta)


def nueva_partida() -> None:
    config, diccionario = _cargar(str(RUTA_JSON))
    ss = st.session_state
    ss.config = config
    ss.tablero = generar_tablero(diccionario, config)
    ss.reloj = Temporizador(config["tiempo_segundos"])
    ss.reloj.iniciar()
    ss.encontradas = []
    ss.mensaje = None
    ss.fase = "jugando"


def terminar() -> None:
    st.session_state.fase = "fin"


def al_enviar() -> None:
    """Callback del formulario: valida la palabra y guarda el mensaje."""
    ss = st.session_state
    texto = ss.get("entrada", "")
    if ss.reloj.terminado:
        ss.fase = "fin"
        return
    res = validar_palabra(texto, ss.tablero, set(ss.encontradas),
                          ss.config["longitud_minima"])
    if not res.valida:
        ss.mensaje = ("error", res.mensaje)
        return
    norm = normalizar(texto)
    ss.encontradas.append(norm)
    pts = puntos_palabra(norm, ss.tablero, ss.config)
    extra = " ⭐ ¡PANGRAMA!" if norm in ss.tablero.pangramas else ""
    ss.mensaje = ("ok", f"**{ss.tablero.palabras[norm]}**  +{pts}{extra}")


def al_mezclar() -> None:
    st.session_state.tablero.mezclar()


# ------------------------------------------------------------- componentes
def panal_html(tablero) -> str:
    w, h, dist = 84, 73, 78
    cx, cy = 150, 140
    celdas = [(cx - w / 2, cy - h / 2, tablero.central, "central")]
    for i, letra in enumerate(tablero.externas):
        ang = math.radians(-90 + 60 * i)
        x = cx + dist * math.cos(ang) - w / 2
        y = cy + dist * math.sin(ang) - h / 2
        celdas.append((x, y, letra, ""))
    hexes = "".join(
        f'<div class="hex {cls}" style="left:{x:.0f}px;top:{y:.0f}px">{letra}</div>'
        for x, y, letra, cls in celdas
    )
    return f'{CSS}<div class="panal">{hexes}</div>'


@st.fragment(run_every=1)
def mostrar_tiempo() -> None:
    """Se refresca sola cada segundo; al acabar el tiempo fuerza el fin."""
    reloj = st.session_state.reloj
    if reloj.terminado:
        st.session_state.fase = "fin"
        st.rerun()
    st.metric("⏱ Tiempo", reloj.formateado())


def lista_palabras(encontradas, tablero) -> str:
    items = []
    for norm in sorted(encontradas):
        txt = tablero.palabras[norm]
        items.append(f"⭐ **{txt}**" if norm in tablero.pangramas else txt)
    return " · ".join(items) if items else "_Aún no has encontrado ninguna._"


# ------------------------------------------------------------------ fases
def pantalla_inicio() -> None:
    config, _ = _cargar(str(RUTA_JSON))
    st.title("🐝 Palabreto")
    st.markdown(
        f"""
- Forma palabras con las **7 letras** del panal.
- Todas deben incluir la **letra central** (amarilla).
- Mínimo **{config['longitud_minima']} letras**; las letras se pueden repetir.
- Hay palabras que usan las 7 letras: ¡son **pangramas**! (+{config['puntos_pangrama']} puntos)
- Tienes **{config['tiempo_segundos'] // 60}:{config['tiempo_segundos'] % 60:02d}** minutos.
"""
    )
    st.button("▶ Empezar", type="primary", on_click=nueva_partida)


def pantalla_juego() -> None:
    ss = st.session_state
    tablero, config = ss.tablero, ss.config
    maximo = puntos_maximos(tablero, config)
    pts = puntos_totales(ss.encontradas, tablero, config)

    izq, der = st.columns([1, 1])

    with izq:
        mostrar_tiempo()
        st.markdown(panal_html(tablero), unsafe_allow_html=True)

        with st.form("form_palabra", clear_on_submit=True, border=False):
            st.text_input("Tu palabra", key="entrada", label_visibility="collapsed",
                          placeholder="Escribe una palabra y pulsa Enter")
            st.form_submit_button("Enviar", on_click=al_enviar, type="primary")

        if ss.mensaje:
            tipo, texto = ss.mensaje
            (st.success if tipo == "ok" else st.error)(texto)

        c1, c2 = st.columns(2)
        c1.button("🔀 Mezclar", on_click=al_mezclar, use_container_width=True)
        c2.button("🏳 Rendirse", on_click=terminar, use_container_width=True)

    with der:
        st.subheader(rango(pts, maximo))
        st.progress(min(1.0, pts / maximo) if maximo else 0.0,
                    text=f"{pts} / {maximo} puntos")
        st.caption(f"{len(ss.encontradas)} de {len(tablero.palabras)} palabras")
        st.markdown(lista_palabras(ss.encontradas, tablero))


def pantalla_fin() -> None:
    ss = st.session_state
    tablero, config = ss.tablero, ss.config
    maximo = puntos_maximos(tablero, config)
    pts = puntos_totales(ss.encontradas, tablero, config)

    st.title("🏁 ¡Fin de la partida!")
    st.metric("Puntuación", f"{pts} / {maximo}", help=rango(pts, maximo))
    st.subheader(rango(pts, maximo))
    st.caption(f"Letras: {tablero.central} (central) + {' '.join(sorted(tablero.externas))}")

    col_ok, col_no = st.columns(2)
    with col_ok:
        st.markdown("**✅ Encontradas**")
        st.markdown(lista_palabras(ss.encontradas, tablero))
    with col_no:
        st.markdown("**❌ Te faltaron**")
        faltan = set(tablero.palabras) - set(ss.encontradas)
        st.markdown(lista_palabras(faltan, tablero) if faltan else "_¡Ninguna!_")

    st.button("🔄 Nueva partida", type="primary", on_click=nueva_partida)


def main() -> None:
    st.set_page_config(page_title="Palabreto", page_icon="🐝", layout="centered")
    fase = st.session_state.get("fase", "inicio")
    {"inicio": pantalla_inicio, "jugando": pantalla_juego, "fin": pantalla_fin}[fase]()
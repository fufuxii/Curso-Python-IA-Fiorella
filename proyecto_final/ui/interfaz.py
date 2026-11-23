import random

import streamlit as st

from ui.estilo import aplicar_estilos

from src.logic.generador import generar_tablero
from src.logic.puntuacion import puntos_palabra
from src.logic.validador import validar_palabra
from src.logic.temporizador import Temporizador


def nueva_partida():

    st.session_state.tablero = generar_tablero()

    st.session_state.reloj = Temporizador()
    st.session_state.reloj.iniciar()

    st.session_state.palabras = []
    st.session_state.puntos = 0
    st.session_state.mensaje = None
    st.session_state.motivo_fin = ""
    st.session_state.reglas_abiertas = False

    st.session_state.fase = "jugando"


def terminar_partida():
    st.session_state.motivo_fin = "manual"
    st.session_state.fase = "fin"


def alternar_reglas():
    st.session_state.reglas_abiertas = not st.session_state.reglas_abiertas


def salir():
    st.session_state.fase = "inicio"


def mezclar_letras():
    random.shuffle(st.session_state.tablero.externas)


def enviar_palabra():

    tablero = st.session_state.tablero
    palabra = st.session_state.get("entrada", "").strip().lower()

    if st.session_state.reloj.terminado:
        st.session_state.motivo_fin = "tiempo"
        st.session_state.fase = "fin"

    elif not palabra:
        st.session_state.mensaje = ("warning", "Escribe una palabra.")

    elif palabra in st.session_state.palabras:
        st.session_state.mensaje = (
            "warning",
            "Ya has encontrado esa palabra."
        )

    elif validar_palabra(palabra, tablero.letras, tablero.central):
        puntos = puntos_palabra(palabra)

        st.session_state.palabras.append(palabra)
        st.session_state.puntos += puntos
        st.session_state.reloj.registrar_palabra()

        st.session_state.mensaje = (
            "success",
            f"¡Palabra correcta! +{puntos} puntos"
        )

    else:
        st.session_state.mensaje = ("error", "Palabra no válida.")


@st.fragment(run_every=1)
def mostrar_tiempo():

    if st.session_state.fase != "jugando":
        return

    reloj = st.session_state.reloj

    if reloj.terminado:
        st.session_state.motivo_fin = "tiempo"
        st.session_state.fase = "fin"
        st.rerun()

    st.metric("⏱ Tiempo restante", reloj.formateado())

    progreso = reloj.restante() / reloj.duracion
    st.progress(min(1.0, max(0.0, progreso)))


def mostrar_panal(tablero):
    hexagonos = "".join(
        f'<div class="hex p{i}">{letra.upper()}</div>'
        for i, letra in enumerate(tablero.externas)
    )

    central = (
        f'<div class="hex central pc">'
        f'{tablero.central.upper()}'
        f'</div>'
    )

    st.markdown(
        f'<div class="panal">{hexagonos}{central}</div>',
        unsafe_allow_html=True
    )


def mostrar_reglas():
    st.markdown("""
    - El panal tiene **7 letras**.
    - Todas las palabras deben contener la **letra central**.
    - Las palabras deben tener **3 letras como mínimo**.
    - Puedes repetir las letras.
    - Las tildes se ignoran al formar palabras.
    - Cada letra de una palabra vale **1 punto**.
    - Tienes **60 segundos** para encontrar una palabra.
    - Cada 5 palabras encontradas, el tiempo disponible
      por palabra se reduce en 10 segundos.
    - El tiempo mínimo será siempre de **10 segundos**.
    """)


def mostrar_palabras(palabras):
    if palabras:
        chips = "".join(
            f'<span class="chip">{palabra}</span>'
            for palabra in reversed(palabras)
        )

        st.markdown(
            f'<div class="palabras">{chips}</div>',
            unsafe_allow_html=True
        )
    else:
        st.caption("Todavía no has encontrado ninguna palabra.")


def barra_lateral():
    with st.sidebar:
        st.markdown(
            '<div class="titulo">🐝 Palabreto</div>',
            unsafe_allow_html=True
        )

        st.markdown("#### 📖 Reglas")
        mostrar_reglas()

        st.divider()

        st.button(
            "🏁 Ver resultados",
            on_click=terminar_partida,
            key="btn_resultados"
        )

        st.button("🚪 Salir", on_click=salir, key="btn_salir")


def vista_previa():

    hexagonos = "".join(
        f'<div class="hex p{i}">{letra}</div>'
        for i, letra in enumerate("REANTO")
    )

    html = "".join([
        '<div class="vista">',
        '<div class="vista-caja">',
        '<div class="vista-metrica"><small>⏱ Tiempo restante</small><b>1:00</b></div>',
        '<div class="vista-barra"><span></span></div>',
        f'<div class="panal">{hexagonos}<div class="hex central pc">S</div></div>',
        '<div class="vista-boton">🔀 Mezclar letras</div>',
        '</div>',
        '<div class="vista-caja">',
        '<div class="vista-fila">',
        '<div class="vista-metrica"><small>⭐ Puntuación</small><b>0</b></div>',
        '<div class="vista-metrica"><small>📝 Palabras</small><b>0</b></div>',
        '</div>',
        '<div class="vista-titulo">✏️ Escribe una palabra</div>',
        '<div class="vista-fila">',
        '<div class="vista-input">Introduce una palabra...</div>',
        '<div class="vista-enviar">Enviar</div>',
        '</div>',
        '<div class="vista-titulo">📚 Palabras encontradas</div>',
        '</div>',
        '</div>',
    ])

    st.markdown(html, unsafe_allow_html=True)


def pantalla_inicio():

    st.markdown(
        '<div class="titulo compacto">🐝 Palabreto</div>',
        unsafe_allow_html=True
    )

    col_vista, col_reglas = st.columns([2.3, 1], gap="large")

    with col_vista:
        with st.container(key="inicio_wrap"):
            vista_previa()

            with st.container(key="inicio_overlay"):
                st.markdown(
                    '<div class="lema">'
                    '¡Encuentra todas las palabras que puedas!'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.button(
                    "▶ Empezar partida",
                    on_click=nueva_partida,
                    type="primary",
                    key="btn_empezar"
                )

    with col_reglas:
        with st.expander("📖 Reglas del juego", expanded=True):
            mostrar_reglas()


def pantalla_juego():

    tablero = st.session_state.tablero

    if "reglas_abiertas" not in st.session_state:
        st.session_state.reglas_abiertas = False

    barra_lateral()

    if st.session_state.mensaje:
        tipo, texto = st.session_state.mensaje
        iconos = {"success": "✅", "warning": "⚠️", "error": "❌"}
        st.toast(texto, icon=iconos[tipo])
        st.session_state.mensaje = None

    st.markdown(
        '<div class="titulo compacto">🐝 Panel de palabras</div>',
        unsafe_allow_html=True
    )

    izquierda, derecha = st.columns(2, gap="large")

    with izquierda:
        with st.container(border=True):
            mostrar_tiempo()
            mostrar_panal(tablero)

            st.button(
                "🔀 Mezclar letras",
                on_click=mezclar_letras,
                key="btn_mezclar"
            )

    with derecha:
        with st.container(border=True):
            col_puntos, col_palabras = st.columns(2)

            with col_puntos:
                st.metric("⭐ Puntuación", st.session_state.puntos)

            with col_palabras:
                st.metric("📝 Palabras", len(st.session_state.palabras))

            st.markdown("##### ✏️ Escribe una palabra")

            with st.form("formulario_palabra", clear_on_submit=True):
                c_input, c_boton = st.columns([3, 1.3])

                with c_input:
                    st.text_input(
                        "Tu palabra",
                        key="entrada",
                        placeholder="Mín. 3 letras + letra central",
                        label_visibility="collapsed"
                    )

                with c_boton:
                    st.form_submit_button(
                        "Enviar",
                        type="primary",
                        on_click=enviar_palabra
                    )

            st.markdown("##### 📚 Palabras encontradas")
            mostrar_palabras(st.session_state.palabras)

        col_reglas, col_terminar = st.columns(2, gap="medium")

        with col_reglas:
            texto_reglas = (
                "📖 Ocultar reglas"
                if st.session_state.reglas_abiertas
                else "📖 Reglas"
            )
            st.button(
                texto_reglas,
                on_click=alternar_reglas,
                key="btn_reglas"
            )

        with col_terminar:
            st.button(
                "🏁 Terminar partida",
                on_click=terminar_partida,
                key="btn_terminar"
            )

        if st.session_state.reglas_abiertas:
            with st.container(border=True):
                mostrar_reglas()


def pantalla_fin():
    _, centro, _ = st.columns([1, 2, 1])

    with centro:
        st.markdown(
            '<div class="titulo">🏁 ¡Fin de la partida!</div>',
            unsafe_allow_html=True
        )

        if st.session_state.motivo_fin == "tiempo":
            motivo = "Se acabó el tiempo."
        else:
            motivo = "Has terminado la partida."

        st.markdown(
            f'<div class="subtitulo">{motivo}</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        col1.metric("⭐ Puntuación final", st.session_state.puntos)
        col2.metric("📝 Palabras", len(st.session_state.palabras))

        st.subheader("📚 Tus palabras")
        mostrar_palabras(st.session_state.palabras)

        st.divider()

        _, col_nueva, col_salir, _ = st.columns(
            [0.5, 2.2, 1.5, 0.5],
            gap="medium"
        )

        with col_nueva:
            st.button(
                "🔄 Nueva partida",
                on_click=nueva_partida,
                type="primary",
                key="btn_nueva"
            )

        with col_salir:
            st.button("🚪 Salir", on_click=salir, key="btn_salir_fin")


def main():
    st.set_page_config(
        page_title="Palabreto",
        page_icon="🐝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    aplicar_estilos()

    if "fase" not in st.session_state:
        st.session_state.fase = "inicio"

    if st.session_state.fase == "inicio":
        pantalla_inicio()

    elif st.session_state.fase == "jugando":
        pantalla_juego()

    elif st.session_state.fase == "fin":
        pantalla_fin()

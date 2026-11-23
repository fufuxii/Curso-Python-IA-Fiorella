import streamlit as st

from src.logic.generador import generar_tablero
from src.logic.puntuacion import puntos_palabra
from src.logic.validador import validar_palabra
from src.logic.temporizador import Temporizador


def nueva_partida():
    """Inicializa una nueva partida."""

    st.session_state.tablero = generar_tablero()

    st.session_state.reloj = Temporizador()
    st.session_state.reloj.iniciar()

    st.session_state.palabras = []
    st.session_state.puntos = 0
    st.session_state.mensaje = ""

    st.session_state.fase = "jugando"


@st.fragment(run_every=1)
def mostrar_tiempo():
    """Se refresca sola cada segundo (requiere Streamlit >= 1.37)."""

    if st.session_state.fase != "jugando":
        return

    reloj = st.session_state.reloj

    if reloj.terminado:
        st.session_state.fase = "fin"
        st.rerun()  # recarga toda la app para mostrar la pantalla final

    st.metric("⏱ Tiempo restante", reloj.formateado())


def mostrar_panal(tablero):
    """Muestra las siete letras del panal: 2 - 3 (con la central en medio) - 2."""

    st.markdown(
        """
        <style>
        .letra {
            background-color: #eeeeee;
            color: #333333;
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            font-size: 25px;
            font-weight: bold;
            margin: 4px;
        }

        .central {
            background-color: #e8a0c4;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    externas = tablero.externas

    def celda(columna, letra, clase="letra"):
        columna.markdown(
            f'<div class="{clase}">{letra.upper()}</div>',
            unsafe_allow_html=True
        )

    # Fila 1: 2 letras (centradas)
    c = st.columns([1, 1, 1, 1])
    celda(c[1], externas[0])
    celda(c[2], externas[1])

    # Fila 2: letra, CENTRAL, letra
    c = st.columns(3)
    celda(c[0], externas[2])
    celda(c[1], tablero.central, "letra central")
    celda(c[2], externas[3])

    # Fila 3: 2 letras (centradas)
    c = st.columns([1, 1, 1, 1])
    celda(c[1], externas[4])
    celda(c[2], externas[5])


def pantalla_inicio():
    """Pantalla inicial con las reglas."""

    st.title("🐝 Palabreto")

    st.write("¡Encuentra todas las palabras que puedas!")

    st.subheader("Reglas del juego")

    st.markdown("""
    - El panal tiene **7 letras**.
    - Todas las palabras deben contener la **letra central**.
    - Las palabras deben tener **3 letras como mínimo**.
    - Puedes repetir las letras.
    - Las tildes se ignoran al formar palabras.
    - Cada letra de una palabra vale **1 punto**.
    - Tienes **60 segundos** para encontrar una palabra.
    - Cada 5 palabras encontradas se restan 10 segundos
      al tiempo disponible por palabra.
    - El tiempo mínimo será siempre de **10 segundos**.
    """)

    st.button(
        "▶ Empezar partida",
        on_click=nueva_partida,
        type="primary"
    )


def pantalla_juego():
    """Interfaz principal de la partida."""

    tablero = st.session_state.tablero

    # Temporizador
    mostrar_tiempo()

    st.divider()

    # Panal
    st.subheader("Tu panal")
    mostrar_panal(tablero)

    st.divider()

    # Entrada de palabras
    with st.form("formulario_palabra", clear_on_submit=True):

        palabra = st.text_input(
            "Escribe una palabra",
            placeholder="Introduce tu palabra..."
        )

        enviar = st.form_submit_button("Enviar palabra")

    if enviar:

        palabra = palabra.strip().lower()

        if st.session_state.reloj.terminado:
            st.session_state.fase = "fin"
            st.rerun()

        elif not palabra:
            st.session_state.mensaje = "⚠️ Escribe una palabra."

        elif palabra in st.session_state.palabras:
            st.session_state.mensaje = "⚠️ Ya has encontrado esa palabra."

        elif validar_palabra(
            palabra,
            tablero.letras,
            tablero.central
        ):

            st.session_state.palabras.append(palabra)

            puntos = puntos_palabra(palabra)

            st.session_state.puntos += puntos

            st.session_state.reloj.registrar_palabra()

            st.session_state.mensaje = (
                f"✅ ¡Palabra correcta! +{puntos} puntos"
            )

        else:
            st.session_state.mensaje = "❌ Palabra no válida."

    # Mensajes
    if st.session_state.mensaje:
        st.info(st.session_state.mensaje)

    st.divider()

    # Puntuación
    col1, col2 = st.columns(2)

    col1.metric("⭐ Puntuación", st.session_state.puntos)

    col2.metric("📝 Palabras", len(st.session_state.palabras))

    # Palabras encontradas
    st.subheader("Palabras encontradas")

    if st.session_state.palabras:
        st.write(", ".join(st.session_state.palabras))
    else:
        st.caption("Todavía no has encontrado ninguna palabra.")


def pantalla_fin():
    """Resultados de la partida."""

    st.title("🏁 ¡Fin de la partida!")

    st.metric("Puntuación final", st.session_state.puntos)

    st.metric(
        "Palabras encontradas",
        len(st.session_state.palabras)
    )

    st.subheader("Tus palabras")

    if st.session_state.palabras:
        st.write(", ".join(st.session_state.palabras))
    else:
        st.write("No has encontrado ninguna palabra.")

    st.button(
        "🔄 Nueva partida",
        on_click=nueva_partida,
        type="primary"
    )


def main():
    """Punto de entrada de la interfaz."""

    st.set_page_config(
        page_title="Palabreto",
        page_icon="🐝",
        layout="centered"
    )

    if "fase" not in st.session_state:
        st.session_state.fase = "inicio"

    if st.session_state.fase == "inicio":
        pantalla_inicio()

    elif st.session_state.fase == "jugando":
        pantalla_juego()

    elif st.session_state.fase == "fin":
        pantalla_fin()

import streamlit as st

COLOR = "#e0709f"
COLOR_OSCURO = "#c95a89"

ESTILOS = f"""

<style>
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stAppDeployButton,
#MainMenu,
footer {{
    display: none !important;
    visibility: hidden !important;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 1rem;
    max-width: 1100px;
}}

[data-testid="stVerticalBlock"] {{
    gap: 1.3rem;
}}

.titulo {{
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 0;
}}

.titulo.compacto {{
    font-size: 2rem;
    margin-bottom: 2rem;
}}

.subtitulo {{
    text-align: center;
    opacity: 0.75;
    margin-bottom: 1.2rem;
}}

.panal {{
    position: relative;
    width: 264px;
    height: 260px;
    margin: 20px auto;
}}

.hex {{
    position: absolute;
    width: 96px;
    height: 84px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    font-weight: 800;
    background: #f1e4ec;
    color: #4a3a44;
    clip-path: polygon(
        25% 0, 75% 0, 100% 50%,
        75% 100%, 25% 100%, 0 50%
    );
    transition: filter 0.15s ease, transform 0.15s ease;
}}

.hex:hover {{
    filter: brightness(0.94);
    transform: scale(1.04);
}}

.hex.central {{
    background: {COLOR};
    color: #ffffff;
}}

.p0 {{ left: 84px; top: 0px; }}
.p1 {{ left: 160px; top: 44px; }}
.p2 {{ left: 160px; top: 132px; }}
.p3 {{ left: 84px; top: 176px; }}
.p4 {{ left: 8px; top: 132px; }}
.p5 {{ left: 8px; top: 44px; }}
.pc {{ left: 84px; top: 88px; }}

.palabras {{
    max-height: 110px;
    overflow-y: auto;
    padding-bottom: 15px;
}}

.chip {{
    display: inline-block;
    padding: 5px 14px;
    margin: 3px;
    border-radius: 999px;
    background: rgba(224, 112, 159, 0.15);
    border: 1px solid rgba(224, 112, 159, 0.5);
    font-weight: 600;
}}

[data-testid="stMetric"] {{
    background: rgba(224, 112, 159, 0.10);
    border: 1px solid rgba(224, 112, 159, 0.30);
    border-radius: 14px;
    padding: 10px 16px;
}}

[data-testid="stMetricValue"] {{
    font-size: 1.8rem;
}}

[data-testid="stButton"],
[data-testid="stFormSubmitButton"] {{
    width: 100%;
}}

.stButton > button,
[data-testid="stFormSubmitButton"] > button {{
    border-radius: 12px;
    font-weight: 600;
    width: 100%;
    min-height: 42px;
    white-space: nowrap;
}}

[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"] {{
    background-color: {COLOR};
    border-color: {COLOR};
    color: #ffffff;
}}

[data-testid="stBaseButton-primary"]:hover,
[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
    background-color: {COLOR_OSCURO};
    border-color: {COLOR_OSCURO};
    color: #ffffff;
}}

.stTextInput input {{
    border-radius: 12px;
    font-size: 1.1rem;
    text-align: center;
}}

.stTextInput [data-baseweb]:focus-within,
[data-baseweb="input"]:focus-within,
[data-baseweb="base-input"]:focus-within {{
    border-color: {COLOR} !important;
    box-shadow: none !important;
}}

[data-testid="InputInstructions"] {{
    display: none !important;
}}

[data-testid="stForm"] {{
    border: none;
    padding: 0;
}}

[data-testid="stSidebar"] li {{
    font-size: 0.92rem;
}}
[data-testid="stElementContainer"]:has([data-testid="stButton"]),
[data-testid="stElementContainer"]:has([data-testid="stFormSubmitButton"]),
[data-testid="stElementContainer"]:has([data-testid="stPopover"]) {{
    width: 100% !important;
}}

[data-testid="stPopover"],
[data-testid="stPopover"] > button {{
    width: 100%;
}}

[data-testid="stPopoverBody"] {{
    min-width: 380px;
}}

.block-container h5 {{
    margin-top: 0.5rem;
    margin-bottom: 0.3rem;
}}

.vista {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    filter: blur(6px);
    opacity: 0.6;
    pointer-events: none;
    user-select: none;
}}

.vista-caja {{
    border: 1px solid rgba(128, 128, 128, 0.35);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}}

.vista-fila {{
    display: flex;
    gap: 12px;
}}

.vista-metrica {{
    flex: 1;
    display: flex;
    flex-direction: column;
    background: rgba(224, 112, 159, 0.10);
    border: 1px solid rgba(224, 112, 159, 0.30);
    border-radius: 14px;
    padding: 10px 16px;
}}

.vista-metrica small {{
    font-size: 0.85rem;
}}

.vista-metrica b {{
    font-size: 1.8rem;
    font-weight: 400;
}}

.vista-barra {{
    height: 8px;
    border-radius: 4px;
    background: rgba(128, 128, 128, 0.3);
}}

.vista-barra span {{
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 4px;
    background: #1c83e1;
}}

.vista-titulo {{
    font-size: 1.05rem;
    font-weight: 700;
}}

.vista-input {{
    flex: 3;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    background: rgba(128, 128, 128, 0.15);
}}

.vista-enviar {{
    flex: 1.3;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    background: {COLOR};
    color: #ffffff;
}}

.vista-boton {{
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    border: 1px solid rgba(128, 128, 128, 0.4);
}}

.st-key-inicio_wrap {{
    position: relative;
}}

.st-key-inicio_overlay {{
    position: absolute;
    inset: 0;
    z-index: 10;
    align-items: center;
    justify-content: center;
}}

.st-key-inicio_overlay [data-testid="stElementContainer"]:has([data-testid="stButton"]) {{
    width: auto !important;
}}

.st-key-inicio_overlay .stButton > button {{
    min-width: 260px;
    min-height: 52px;
    font-size: 1.1rem;
}}

.lema {{
    text-align: center;
    font-size: 1.4rem;
    font-weight: 800;
}}
</style>
"""

def aplicar_estilos():
    st.markdown(ESTILOS, unsafe_allow_html=True)

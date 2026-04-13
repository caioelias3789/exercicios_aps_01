import streamlit as st
from enum import Enum

# =========================
# ENUMERAÇÕES
# =========================

class EnumCor(Enum):
    PRETO = "black"
    BRANCO = "white"
    AZUL = "blue"
    AMARELO = "yellow"
    CINZA = "gray"

class EnumTipo(Enum):
    LABEL = "Label"
    EDIT = "Edit"
    MEMO = "Memo"

# =========================
# FUNÇÃO DE RENDERIZAÇÃO
# =========================

def renderizar_texto(texto, tam_letra, cor_fonte, cor_fundo):
    estilo = f"""
        <div style="
            font-size: {tam_letra}px;
            color: {cor_fonte};
            background-color: {cor_fundo};
            padding: 10px;
            border-radius: 5px;
        ">
            {texto}
        </div>
    """
    st.markdown(estilo, unsafe_allow_html=True)

# =========================
# INTERFACE STREAMLIT
# =========================

st.title("Sistema de Formatação de Texto")

# Entrada de dados
st.sidebar.header("Configurações")

tam_letra = st.sidebar.number_input(
    "Tamanho da Letra",
    min_value=8,
    max_value=72,
    value=16
)

cor_fonte = st.sidebar.selectbox(
    "Cor da Fonte",
    list(EnumCor)
)

cor_fundo = st.sidebar.selectbox(
    "Cor de Fundo",
    list(EnumCor)
)

tipo_comp = st.sidebar.selectbox(
    "Tipo de Componente",
    list(EnumTipo)
)

# Campo de texto dependendo do tipo
st.header("Entrada de Texto")

if tipo_comp == EnumTipo.LABEL:
    texto = st.text_input("Texto (Label)")

elif tipo_comp == EnumTipo.EDIT:
    texto = st.text_input("Texto (Edit)")

elif tipo_comp == EnumTipo.MEMO:
    texto = st.text_area("Texto (Memo)", height=150)

# =========================
# SAÍDA
# =========================

st.header("TEXTO_SAIDA")

if texto:
    renderizar_texto(
        texto,
        tam_letra,
        cor_fonte.value,
        cor_fundo.value
    )
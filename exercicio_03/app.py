import streamlit as st
from enum import Enum

# Enum Direcao
class Direcao(Enum):
    CIMA = "CIMA"
    BAIXO = "BAIXO"
    DIREITA = "DIREITA"
    ESQUERDA = "ESQUERDA"

# Classe Boneco
class Boneco:
    def __init__(self, nome):
        self.nome = nome
        self.coordX = 0
        self.coordY = 0
        self.direcao = Direcao.CIMA

    def mover(self, direcao):
        self.direcao = direcao
        
        if direcao == Direcao.CIMA:
            self.coordY += 1
        elif direcao == Direcao.BAIXO:
            self.coordY -= 1
        elif direcao == Direcao.DIREITA:
            self.coordX += 1
        elif direcao == Direcao.ESQUERDA:
            self.coordX -= 1

    def moverCima(self):
        self.mover(Direcao.CIMA)

    def moverBaixo(self):
        self.mover(Direcao.BAIXO)

    def moverDireita(self):
        self.mover(Direcao.DIREITA)

    def moverEsquerda(self):
        self.mover(Direcao.ESQUERDA)

    def getPosicao(self):
        return self.coordX, self.coordY

    def setDirecao(self, direcao):
        self.direcao = direcao


# ---------------- STREAMLIT ---------------- #

st.title("🎮 Controle do Boneco")

# Criar boneco na sessão
if "boneco" not in st.session_state:
    st.session_state.boneco = None

# Criar boneco
nome = st.text_input("Nome do Boneco:")

if st.button("Criar Boneco"):
    if nome:
        st.session_state.boneco = Boneco(nome)
        st.success("Boneco criado!")
    else:
        st.warning("Digite um nome!")

# Se já existe boneco
if st.session_state.boneco:
    boneco = st.session_state.boneco

    st.subheader(f"Boneco: {boneco.nome}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬆️ Cima"):
            boneco.moverCima()
        if st.button("⬇️ Baixo"):
            boneco.moverBaixo()

    with col2:
        if st.button("➡️ Direita"):
            boneco.moverDireita()
        if st.button("⬅️ Esquerda"):
            boneco.moverEsquerda()

    x, y = boneco.getPosicao()

    st.write(f"📍 Posição X: {x}")
    st.write(f"📍 Posição Y: {y}")
    st.write(f"🧭 Direção atual: {boneco.direcao.value}")
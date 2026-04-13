import streamlit as st
from datetime import datetime, timedelta, time

# =========================
# Classe Horario
# =========================
class Horario:
    def __init__(self, hora):
        self.hora = hora
        self.tomado = False
        self.atrasado = False

    def remarcar(self, nova_hora):
        self.hora = nova_hora

    def exibir(self):
        status = "✔️ Tomado" if self.tomado else "⏳ Pendente"
        if self.atrasado:
            status += " (Atrasado)"
        return f"{self.hora.strftime('%H:%M')} - {status}"


# =========================
# Classe Remedio
# =========================
class Remedio:
    def __init__(self, nomePaciente, dataInicio, qtdDias, vezesAoDia, dosagem, nomeRemedio):
        self.nomePaciente = nomePaciente
        self.dataInicio = dataInicio
        self.qtdDias = qtdDias
        self.vezesAoDia = vezesAoDia
        self.dosagem = dosagem
        self.nomeRemedio = nomeRemedio
        self.horarios = []

    def cadastrar(self):
        return f"Remédio {self.nomeRemedio} cadastrado para {self.nomePaciente}"

    def sugerirHorario(self):
        intervalo = 24 // self.vezesAoDia
        horarios = []
        for i in range(self.vezesAoDia):
            hora = time(hour=(8 + i * intervalo) % 24, minute=0)
            horarios.append(Horario(hora))
        self.horarios = horarios

    def calcularDataFim(self):
        return self.dataInicio + timedelta(days=self.qtdDias)

    def gerarPlanilha(self):
        dados = []
        data = self.dataInicio

        for dia in range(self.qtdDias):
            for h in self.horarios:
                dados.append({
                    "Data": data.strftime("%d/%m/%Y"),
                    "Hora": h.hora.strftime("%H:%M"),
                    "Medicamento": self.nomeRemedio,
                    "Dosagem": self.dosagem
                })
            data += timedelta(days=1)

        return dados

    def reorganizarHorarios(self):
        self.horarios.sort(key=lambda h: h.hora)


# =========================
# Interface Streamlit
# =========================
st.title("💊 Controle de Medicamentos")

st.sidebar.header("Cadastro do Remédio")

nomePaciente = st.sidebar.text_input("Nome do Paciente")
nomeRemedio = st.sidebar.text_input("Nome do Remédio")
dosagem = st.sidebar.text_input("Dosagem")
dataInicio = st.sidebar.date_input("Data de Início")
qtdDias = st.sidebar.number_input("Quantidade de Dias", min_value=1)
vezesAoDia = st.sidebar.number_input("Vezes ao Dia", min_value=1, max_value=24)

if st.sidebar.button("Cadastrar"):
    remedio = Remedio(
        nomePaciente,
        dataInicio,
        qtdDias,
        vezesAoDia,
        dosagem,
        nomeRemedio
    )

    remedio.sugerirHorario()
    remedio.reorganizarHorarios()

    st.session_state["remedio"] = remedio
    st.success(remedio.cadastrar())


# =========================
# Exibição
# =========================
if "remedio" in st.session_state:
    remedio = st.session_state["remedio"]

    st.subheader("📋 Informações")
    st.write(f"Paciente: {remedio.nomePaciente}")
    st.write(f"Remédio: {remedio.nomeRemedio}")
    st.write(f"Dosagem: {remedio.dosagem}")
    st.write(f"Data fim: {remedio.calcularDataFim()}")

    st.subheader("⏰ Horários")
    for i, h in enumerate(remedio.horarios):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(h.exibir())

        with col2:
            if st.button(f"Tomado {i}"):
                h.tomado = True

        with col3:
            if st.button(f"Atrasado {i}"):
                h.atrasado = True

    st.subheader("📊 Planilha")
    dados = remedio.gerarPlanilha()
    st.dataframe(dados)
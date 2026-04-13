import streamlit as st
from enum import Enum
from datetime import date

# ---------------- ENUMS ---------------- #

class Tipo_de_Gasto(Enum):
    ROUPAS = "ROUPAS"
    REMEDIO = "REMEDIO"
    ALIMENTACAO = "ALIMENTACAO"

class FormaPagamento(Enum):
    DINHEIRO = "DINHEIRO"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    TICKET_ALIMENTACAO = "TICKET_ALIMENTACAO"
    VALE_REFEICAO = "VALE_REFEICAO"

# ---------------- CLASSE GASTO ---------------- #

class Gasto:
    def __init__(self, tipo, data, valor, formaPagamento):
        self.tipo = tipo
        self.data = data
        self.valor = valor
        self.formaPagamento = formaPagamento

    def cadastrar(self):
        return "Gasto cadastrado com sucesso!"

    def exibir(self):
        return f"{self.data} | {self.tipo.value} | R$ {self.valor:.2f} | {self.formaPagamento.value}"

# ---------------- CLASSE CONTROLE ---------------- #

class ControleGastos:
    def __init__(self):
        self.gasto_list = []

    def adicionarGasto(self, gasto):
        self.gasto_list.append(gasto)

    def calcularTotalMensal(self):
        return sum(g.valor for g in self.gasto_list)

    def agruparPorTipo(self):
        resultado = {}
        for g in self.gasto_list:
            resultado[g.tipo] = resultado.get(g.tipo, 0) + g.valor
        return resultado

    def totalPorFormaPagamento(self):
        resultado = {}
        for g in self.gasto_list:
            resultado[g.formaPagamento] = resultado.get(g.formaPagamento, 0) + g.valor
        return resultado


# ---------------- STREAMLIT ---------------- #

st.title("💰 Controle de Gastos")

# Inicializar controle
if "controle" not in st.session_state:
    st.session_state.controle = ControleGastos()

controle = st.session_state.controle

# ---------- FORMULÁRIO ---------- #
st.subheader("➕ Adicionar Gasto")

tipo = st.selectbox("Tipo", list(Tipo_de_Gasto))
data_gasto = st.date_input("Data", value=date.today())
valor = st.number_input("Valor", min_value=0.0, format="%.2f")
forma = st.selectbox("Forma de Pagamento", list(FormaPagamento))

if st.button("Cadastrar Gasto"):
    gasto = Gasto(tipo, data_gasto, valor, forma)
    controle.adicionarGasto(gasto)
    st.success(gasto.cadastrar())

# ---------- LISTAGEM ---------- #
st.subheader("📋 Lista de Gastos")

if controle.gasto_list:
    for g in controle.gasto_list:
        st.write(g.exibir())
else:
    st.info("Nenhum gasto cadastrado.")

# ---------- TOTAL ---------- #
st.subheader("💵 Total Mensal")
total = controle.calcularTotalMensal()
st.write(f"Total: R$ {total:.2f}")

# ---------- AGRUPAMENTO POR TIPO ---------- #
st.subheader("📊 Total por Tipo")

dados_tipo = controle.agruparPorTipo()
for tipo, valor in dados_tipo.items():
    st.write(f"{tipo.value}: R$ {valor:.2f}")

# ---------- AGRUPAMENTO POR FORMA ---------- #
st.subheader("💳 Total por Forma de Pagamento")

dados_forma = controle.totalPorFormaPagamento()
for forma, valor in dados_forma.items():
    st.write(f"{forma.value}: R$ {valor:.2f}")
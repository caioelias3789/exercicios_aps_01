import streamlit as st

# ---------------- CLASSE CD ---------------- #

class CD:
    def __init__(self, cantorOuConjunto, titulo, anoLancamento):
        self.cantorOuConjunto = cantorOuConjunto
        self.titulo = titulo
        self.anoLancamento = anoLancamento

    def cadastrar(self):
        return "CD cadastrado com sucesso!"

    def exibir(self):
        return f"{self.titulo} - {self.cantorOuConjunto} ({self.anoLancamento})"


# ---------------- CLASSE COLECAO ---------------- #

class ColecaoCD:
    def __init__(self):
        self.cds = []

    def adicionarCD(self, cd):
        self.cds.append(cd)

    def listarCDs(self):
        return [cd.exibir() for cd in self.cds]

    def buscarPorTitulo(self, titulo):
        for cd in self.cds:
            if cd.titulo.lower() == titulo.lower():
                return cd
        return None

    def buscarPorCantor(self, nome):
        return [cd for cd in self.cds if nome.lower() in cd.cantorOuConjunto.lower()]


# ---------------- STREAMLIT ---------------- #

st.set_page_config(layout="wide")
st.title("💿 Coleção de CDs")

# Estado
if "colecao" not in st.session_state:
    st.session_state.colecao = ColecaoCD()

colecao = st.session_state.colecao

# -------- ADICIONAR CD -------- #
st.subheader("➕ Cadastrar CD")

col1, col2 = st.columns(2)

with col1:
    cantor = st.text_input("Cantor / Banda")
    titulo = st.text_input("Título")

with col2:
    ano = st.number_input("Ano de Lançamento", min_value=1900, max_value=2100, step=1)

if st.button("Cadastrar CD"):
    if cantor and titulo:
        cd = CD(cantor, titulo, ano)
        colecao.adicionarCD(cd)
        st.success(cd.cadastrar())
    else:
        st.warning("Preencha todos os campos!")

# -------- LISTAR -------- #
st.subheader("📋 Lista de CDs")

if colecao.cds:
    for cd in colecao.cds:
        st.write(cd.exibir())
else:
    st.info("Nenhum CD cadastrado.")

# -------- BUSCAR -------- #
st.subheader("🔍 Buscar CD")

tipo_busca = st.radio("Buscar por:", ["Título", "Cantor/Banda"])

busca = st.text_input("Digite para buscar")

if st.button("Buscar"):
    if tipo_busca == "Título":
        resultado = colecao.buscarPorTitulo(busca)
        if resultado:
            st.success(resultado.exibir())
        else:
            st.error("CD não encontrado.")
    else:
        resultados = colecao.buscarPorCantor(busca)
        if resultados:
            for cd in resultados:
                st.write(cd.exibir())
        else:
            st.error("Nenhum resultado encontrado.")

# -------- REMOVER -------- #
st.subheader("❌ Remover CD")

if colecao.cds:
    opcoes = [cd.exibir() for cd in colecao.cds]
    escolha = st.selectbox("Selecione um CD", opcoes)

    if st.button("Remover"):
        index = opcoes.index(escolha)
        colecao.cds.pop(index)
        st.success("CD removido!")
        st.rerun()

# -------- ESTATÍSTICAS -------- #
st.subheader("📊 Estatísticas")

if colecao.cds:
    total = len(colecao.cds)
    mais_antigo = min(colecao.cds, key=lambda cd: cd.anoLancamento)
    mais_novo = max(colecao.cds, key=lambda cd: cd.anoLancamento)

    st.write(f"Total de CDs: {total}")
    st.write(f"Mais antigo: {mais_antigo.exibir()}")
    st.write(f"Mais recente: {mais_novo.exibir()}")
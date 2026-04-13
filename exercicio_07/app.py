import streamlit as st

# ---------------- CLASSE ProdutoCompra ---------------- #

class ProdutoCompra:
    def __init__(self, nome, unidadeCompra, qtdMes, qtdCompra, precoEstimado):
        self.nome = nome
        self.unidadeCompra = unidadeCompra
        self.qtdMes = qtdMes
        self.qtdCompra = qtdCompra
        self.precoEstimado = precoEstimado
        self.subtotal = 0.0

    def calcularSubtotal(self):
        self.subtotal = self.qtdCompra * self.precoEstimado
        return self.subtotal

    def atualizarPreco(self, novoPreco):
        self.precoEstimado = novoPreco
        self.calcularSubtotal()

    def exibir(self):
        return f"{self.nome} | {self.qtdCompra} {self.unidadeCompra} | R$ {self.precoEstimado:.2f} | Subtotal: R$ {self.subtotal:.2f}"


# ---------------- CLASSE ListaCompra ---------------- #

class ListaCompra:
    def __init__(self):
        self.itens = []
        self.total = 0.0

    def adicionarProduto(self, produto):
        produto.calcularSubtotal()
        self.itens.append(produto)

    def calcularTotal(self):
        self.total = sum(p.calcularSubtotal() for p in self.itens)
        return self.total

    def listarProdutos(self):
        return [p.exibir() for p in self.itens]

    def atualizarPrecoProduto(self, produto, novoPreco):
        produto.atualizarPreco(novoPreco)


# ---------------- STREAMLIT ---------------- #

st.set_page_config(layout="wide")
st.title("🛒 Lista de Compras Inteligente")

# Estado
if "lista" not in st.session_state:
    st.session_state.lista = ListaCompra()

lista = st.session_state.lista

# -------- ADICIONAR PRODUTO -------- #
st.subheader("➕ Adicionar Produto")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome do Produto")
    unidade = st.selectbox("Unidade", ["kg", "litro", "unidade"])
    qtdMes = st.number_input("Quantidade mensal", min_value=0.0)

with col2:
    qtdCompra = st.number_input("Quantidade para compra", min_value=0.0)
    preco = st.number_input("Preço estimado", min_value=0.0)

if st.button("Adicionar Produto"):
    if nome:
        produto = ProdutoCompra(nome, unidade, qtdMes, qtdCompra, preco)
        lista.adicionarProduto(produto)
        st.success("Produto adicionado!")
    else:
        st.warning("Digite o nome!")

# -------- LISTAGEM -------- #
st.subheader("📋 Produtos")

if lista.itens:
    for i, p in enumerate(lista.itens):
        colA, colB, colC = st.columns([3,1,1])

        with colA:
            st.write(p.nome)

        with colB:
            novo_preco = st.number_input(
                "Preço",
                value=p.precoEstimado,
                key=f"preco_{i}"
            )
            if novo_preco != p.precoEstimado:
                lista.atualizarPrecoProduto(p, novo_preco)

        with colC:
            if st.button("❌", key=f"rem_{i}"):
                lista.itens.pop(i)
                st.rerun()

        p.calcularSubtotal()
        st.write(p.exibir())
        st.divider()
else:
    st.info("Nenhum produto na lista.")

# -------- TOTAL -------- #
st.subheader("💰 Total da Compra")

total = lista.calcularTotal()
st.write(f"### R$ {total:.2f}")
import streamlit as st

# ---------------- CLASSES ---------------- #

class Produto:
    def __init__(self, nome, valorUnitario):
        self.nome = nome
        self.valorUnitario = valorUnitario

    def exibirProduto(self):
        return f"{self.nome} - R$ {self.valorUnitario:.2f}"


class ItemComanda:
    def __init__(self, quantidade, produto):
        self.quantidade = quantidade
        self.produto = produto
        self.subtotal = 0.0

    def calcularSubtotal(self):
        self.subtotal = self.quantidade * self.produto.valorUnitario
        return self.subtotal


class Comanda:
    def __init__(self, numero):
        self.numero = numero
        self.itens = []
        self.total = 0.0

    def registrarProduto(self, produto, quantidade):
        item = ItemComanda(quantidade, produto)
        item.calcularSubtotal()
        self.itens.append(item)

    def removerItem(self, index):
        if 0 <= index < len(self.itens):
            del self.itens[index]

    def calcularTotal(self):
        self.total = sum(item.calcularSubtotal() for item in self.itens)
        return self.total

    def finalizarComanda(self):
        return f"Comanda {self.numero} finalizada! Total: R$ {self.calcularTotal():.2f}"


# ---------------- CARDÁPIO ---------------- #

cardapio = [
    Produto("Hamburguer", 15.0),
    Produto("Pizza", 30.0),
    Produto("Refrigerante", 6.0),
    Produto("Suco", 8.0),
]

# ---------------- STREAMLIT ---------------- #

st.set_page_config(layout="wide")
st.title("🍽️ Sistema de Comanda ")

# Inicialização
if "comandas" not in st.session_state:
    st.session_state.comandas = {}

if "comanda_atual" not in st.session_state:
    st.session_state.comanda_atual = None


# -------- CRIAR COMANDA -------- #
st.sidebar.header("📌 Comandas")

novo_numero = st.sidebar.number_input("Nova Comanda", min_value=1, step=1)

if st.sidebar.button("Criar"):
    if novo_numero not in st.session_state.comandas:
        st.session_state.comandas[novo_numero] = Comanda(novo_numero)
        st.success(f"Comanda {novo_numero} criada!")

# Selecionar comanda
if st.session_state.comandas:
    selecionada = st.sidebar.selectbox(
        "Selecionar Comanda",
        list(st.session_state.comandas.keys())
    )
    st.session_state.comanda_atual = st.session_state.comandas[selecionada]

# -------- ÁREA PRINCIPAL -------- #
if st.session_state.comanda_atual:

    comanda = st.session_state.comanda_atual
    st.subheader(f"🧾 Comanda #{comanda.numero}")

    col1, col2 = st.columns(2)

    # -------- ADICIONAR PRODUTO -------- #
    with col1:
        st.subheader("➕ Adicionar Produto")

        produto_escolhido = st.selectbox(
            "Produto",
            cardapio,
            format_func=lambda p: p.exibirProduto()
        )

        qtd = st.number_input("Quantidade", min_value=1, step=1)

        if st.button("Adicionar"):
            comanda.registrarProduto(produto_escolhido, qtd)
            st.success("Produto adicionado!")

    # -------- LISTA DE ITENS -------- #
    with col2:
        st.subheader("📋 Itens")

        if comanda.itens:
            for i, item in enumerate(comanda.itens):
                colA, colB, colC = st.columns([3,1,1])

                with colA:
                    st.write(f"{item.produto.nome} (R$ {item.produto.valorUnitario:.2f})")

                with colB:
                    nova_qtd = st.number_input(
                        "Qtd",
                        min_value=1,
                        value=item.quantidade,
                        key=f"qtd_{i}"
                    )
                    item.quantidade = nova_qtd
                    item.calcularSubtotal()

                with colC:
                    if st.button("❌", key=f"remover_{i}"):
                        comanda.removerItem(i)
                        st.rerun()

                st.write(f"Subtotal: R$ {item.subtotal:.2f}")
                st.divider()
        else:
            st.info("Nenhum item na comanda.")

    # -------- TOTAL -------- #
    st.subheader("💰 Total")
    total = comanda.calcularTotal()
    st.write(f"### R$ {total:.2f}")

    # -------- FINALIZAR -------- #
    if st.button("✅ Finalizar Comanda"):
        st.success(comanda.finalizarComanda())

else:
    st.info("Crie ou selecione uma comanda no menu lateral.")
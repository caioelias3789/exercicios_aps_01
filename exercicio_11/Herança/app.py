import streamlit as st
from datetime import date, datetime

# =========================
# CLASSES DO MODELO
# =========================

class Endereco:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str, cep: str):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - CEP: {self.cep}"


class Telefone:
    def __init__(self, numero: str, tipo: str):
        self.numero = numero
        self.tipo = tipo

    def __str__(self):
        return f"{self.numero} ({self.tipo})"


class Pessoa:
    def __init__(self, nome: str, dt_nasc: date, endereco: Endereco, telefone: Telefone):
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.endereco = endereco
        self.telefone = telefone

    def cadastrar(self):
        return f"{self.nome} cadastrado com sucesso."

    def obter_idade(self):
        hoje = date.today()
        idade = hoje.year - self.dt_nasc.year
        if (hoje.month, hoje.day) < (self.dt_nasc.month, self.dt_nasc.day):
            idade -= 1
        return idade


class Funcionario(Pessoa):
    def __init__(self, nome: str, dt_nasc: date, endereco: Endereco, telefone: Telefone,
                 matricula: int, cargo: str, salario: float):
        super().__init__(nome, dt_nasc, endereco, telefone)
        self.matricula = matricula
        self.cargo = cargo
        self.salario = salario

    def admitir(self):
        return f"Funcionário {self.nome} admitido com sucesso."

    def reajustar_salario(self, percentual: float):
        self.salario += self.salario * (percentual / 100)

    def promover(self, novo_cargo: str):
        self.cargo = novo_cargo


class Cliente(Pessoa):
    def __init__(self, nome: str, dt_nasc: date, endereco: Endereco, telefone: Telefone,
                 codigo: str, profissao: str):
        super().__init__(nome, dt_nasc, endereco, telefone)
        self.codigo = codigo
        self.profissao = profissao


# =========================
# FUNÇÕES AUXILIARES
# =========================

def inicializar_sessao():
    if "clientes" not in st.session_state:
        st.session_state.clientes = []

    if "funcionarios" not in st.session_state:
        st.session_state.funcionarios = []


def criar_endereco(rua, numero, bairro, cidade, cep):
    return Endereco(rua, numero, bairro, cidade, cep)


def criar_telefone(numero, tipo):
    return Telefone(numero, tipo)


# =========================
# INTERFACE
# =========================

st.set_page_config(page_title="Sistema de Pessoas", layout="wide")
inicializar_sessao()

st.title("Sistema de Cadastro - Pessoa, Cliente e Funcionário")

menu = st.sidebar.selectbox(
    "Escolha uma opção",
    [
        "Cadastrar Cliente",
        "Cadastrar Funcionário",
        "Listar Clientes",
        "Listar Funcionários",
        "Gerenciar Funcionários"
    ]
)

# =========================
# CADASTRAR CLIENTE
# =========================
if menu == "Cadastrar Cliente":
    st.header("Cadastro de Cliente")

    with st.form("form_cliente"):
        st.subheader("Dados da Pessoa")
        nome = st.text_input("Nome")
        dt_nasc = st.date_input("Data de nascimento", min_value=date(1900, 1, 1), max_value=date.today())

        st.subheader("Endereço")
        rua = st.text_input("Rua")
        numero_end = st.number_input("Número", min_value=0, step=1)
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        cep = st.text_input("CEP")

        st.subheader("Telefone")
        numero_tel = st.text_input("Número do telefone")
        tipo_tel = st.selectbox("Tipo", ["Celular", "Residencial", "Comercial"])

        st.subheader("Dados do Cliente")
        codigo = st.text_input("Código")
        profissao = st.text_input("Profissão")

        enviar = st.form_submit_button("Cadastrar Cliente")

        if enviar:
            endereco = criar_endereco(rua, numero_end, bairro, cidade, cep)
            telefone = criar_telefone(numero_tel, tipo_tel)

            cliente = Cliente(
                nome=nome,
                dt_nasc=dt_nasc,
                endereco=endereco,
                telefone=telefone,
                codigo=codigo,
                profissao=profissao
            )

            st.session_state.clientes.append(cliente)
            st.success(cliente.cadastrar())
            st.info(f"Idade de {cliente.nome}: {cliente.obter_idade()} anos")


# =========================
# CADASTRAR FUNCIONÁRIO
# =========================
elif menu == "Cadastrar Funcionário":
    st.header("Cadastro de Funcionário")

    with st.form("form_funcionario"):
        st.subheader("Dados da Pessoa")
        nome = st.text_input("Nome")
        dt_nasc = st.date_input("Data de nascimento", min_value=date(1900, 1, 1), max_value=date.today())

        st.subheader("Endereço")
        rua = st.text_input("Rua")
        numero_end = st.number_input("Número", min_value=0, step=1)
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        cep = st.text_input("CEP")

        st.subheader("Telefone")
        numero_tel = st.text_input("Número do telefone")
        tipo_tel = st.selectbox("Tipo", ["Celular", "Residencial", "Comercial"])

        st.subheader("Dados do Funcionário")
        matricula = st.number_input("Matrícula", min_value=1, step=1)
        cargo = st.text_input("Cargo")
        salario = st.number_input("Salário", min_value=0.0, step=100.0)

        enviar = st.form_submit_button("Cadastrar Funcionário")

        if enviar:
            endereco = criar_endereco(rua, numero_end, bairro, cidade, cep)
            telefone = criar_telefone(numero_tel, tipo_tel)

            funcionario = Funcionario(
                nome=nome,
                dt_nasc=dt_nasc,
                endereco=endereco,
                telefone=telefone,
                matricula=matricula,
                cargo=cargo,
                salario=salario
            )

            st.session_state.funcionarios.append(funcionario)
            st.success(funcionario.cadastrar())
            st.info(funcionario.admitir())
            st.info(f"Idade de {funcionario.nome}: {funcionario.obter_idade()} anos")


# =========================
# LISTAR CLIENTES
# =========================
elif menu == "Listar Clientes":
    st.header("Lista de Clientes")

    if not st.session_state.clientes:
        st.warning("Nenhum cliente cadastrado.")
    else:
        for i, cliente in enumerate(st.session_state.clientes, start=1):
            with st.expander(f"Cliente {i} - {cliente.nome}"):
                st.write(f"**Código:** {cliente.codigo}")
                st.write(f"**Profissão:** {cliente.profissao}")
                st.write(f"**Idade:** {cliente.obter_idade()} anos")
                st.write(f"**Endereço:** {cliente.endereco}")
                st.write(f"**Telefone:** {cliente.telefone}")


# =========================
# LISTAR FUNCIONÁRIOS
# =========================
elif menu == "Listar Funcionários":
    st.header("Lista de Funcionários")

    if not st.session_state.funcionarios:
        st.warning("Nenhum funcionário cadastrado.")
    else:
        for i, funcionario in enumerate(st.session_state.funcionarios, start=1):
            with st.expander(f"Funcionário {i} - {funcionario.nome}"):
                st.write(f"**Matrícula:** {funcionario.matricula}")
                st.write(f"**Cargo:** {funcionario.cargo}")
                st.write(f"**Salário:** R$ {funcionario.salario:.2f}")
                st.write(f"**Idade:** {funcionario.obter_idade()} anos")
                st.write(f"**Endereço:** {funcionario.endereco}")
                st.write(f"**Telefone:** {funcionario.telefone}")


# =========================
# GERENCIAR FUNCIONÁRIOS
# =========================
elif menu == "Gerenciar Funcionários":
    st.header("Gerenciar Funcionários")

    if not st.session_state.funcionarios:
        st.warning("Nenhum funcionário cadastrado.")
    else:
        nomes_funcionarios = [f"{f.nome} - Matrícula {f.matricula}" for f in st.session_state.funcionarios]
        escolha = st.selectbox("Selecione um funcionário", nomes_funcionarios)
        indice = nomes_funcionarios.index(escolha)
        funcionario = st.session_state.funcionarios[indice]

        st.subheader("Dados atuais")
        st.write(f"**Nome:** {funcionario.nome}")
        st.write(f"**Cargo:** {funcionario.cargo}")
        st.write(f"**Salário:** R$ {funcionario.salario:.2f}")

        st.divider()

        st.subheader("Reajustar salário")
        percentual = st.number_input("Percentual de reajuste (%)", min_value=0.0, step=1.0)
        if st.button("Aplicar reajuste"):
            funcionario.reajustar_salario(percentual)
            st.success(f"Novo salário de {funcionario.nome}: R$ {funcionario.salario:.2f}")

        st.divider()

        st.subheader("Promover funcionário")
        novo_cargo = st.text_input("Novo cargo")
        if st.button("Promover"):
            if novo_cargo.strip():
                funcionario.promover(novo_cargo)
                st.success(f"{funcionario.nome} foi promovido para {funcionario.cargo}.")
            else:
                st.error("Digite um novo cargo.")
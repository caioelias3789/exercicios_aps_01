import pandas as pd
import streamlit as st
from datetime import datetime, date
from models import SalaReuniao, Funcionario, Reuniao, AgendaDiaria

st.set_page_config(page_title="Controle de Salas de Reunião", page_icon="📅")
st.title("Controle de Salas de Reunião")

if "salas" not in st.session_state:
    st.session_state.salas = []

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = []

if "agenda" not in st.session_state:
    st.session_state.agenda = AgendaDiaria(date.today())

agenda = st.session_state.agenda

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Cadastrar Sala",
    "Cadastrar Funcionário",
    "Agendar Reunião",
    "Realocar Reunião",
    "Consultas"
])

with tab1:
    st.subheader("Cadastrar sala")

    with st.form("form_sala"):
        numero_sala = st.number_input("Número da sala", min_value=1, step=1)
        lugares = st.number_input("Quantidade de lugares", min_value=1, step=1)
        salvar_sala = st.form_submit_button("Salvar sala")

    if salvar_sala:
        existe = any(s.numero == int(numero_sala) for s in st.session_state.salas)
        if existe:
            st.warning("Já existe uma sala com esse número.")
        else:
            st.session_state.salas.append(SalaReuniao(int(numero_sala), int(lugares)))
            st.success("Sala cadastrada com sucesso!")

    if st.session_state.salas:
        df_salas = pd.DataFrame([s.exibir() for s in st.session_state.salas])
        st.dataframe(df_salas, use_container_width=True)

with tab2:
    st.subheader("Cadastrar funcionário")

    with st.form("form_funcionario"):
        nome = st.text_input("Nome")
        cargo = st.text_input("Cargo")
        ramal = st.text_input("Ramal")
        salvar_func = st.form_submit_button("Salvar funcionário")

    if salvar_func:
        if not nome.strip():
            st.warning("Informe o nome do funcionário.")
        else:
            st.session_state.funcionarios.append(Funcionario(nome, cargo, ramal))
            st.success("Funcionário cadastrado com sucesso!")

    if st.session_state.funcionarios:
        df_func = pd.DataFrame([f.exibir() for f in st.session_state.funcionarios])
        st.dataframe(df_func, use_container_width=True)

with tab3:
    st.subheader("Agendar reunião")

    if not st.session_state.salas:
        st.info("Cadastre pelo menos uma sala.")
    elif not st.session_state.funcionarios:
        st.info("Cadastre pelo menos um funcionário.")
    else:
        with st.form("form_reuniao"):
            assunto = st.text_input("Assunto")
            data_reuniao = st.date_input("Data", value=agenda.data)

            horario_str = st.selectbox(
                "Horário",
                ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]
            )

            sala_numero = st.selectbox(
                "Sala",
                [s.numero for s in st.session_state.salas]
            )

            funcionario_nome = st.selectbox(
                "Funcionário responsável",
                [f.nome for f in st.session_state.funcionarios]
            )

            salvar_reuniao = st.form_submit_button("Agendar")

        if salvar_reuniao:
            sala = next(s for s in st.session_state.salas if s.numero == sala_numero)
            funcionario = next(f for f in st.session_state.funcionarios if f.nome == funcionario_nome)

            horario = datetime.strptime(horario_str, "%H:%M").time()

            if not sala.verificar_disponibilidade(agenda.reunioes, data_reuniao, horario):
                st.error("Essa sala já está ocupada nesse horário.")
            else:
                reuniao = Reuniao(
                    assunto=assunto,
                    data=data_reuniao,
                    horario=horario,
                    sala=sala,
                    funcionario=funcionario
                )
                agenda.adicionar_reuniao(reuniao)
                st.success("Reunião agendada com sucesso!")

with tab4:
    st.subheader("Realocar reunião")

    reunioes = agenda.reunioes

    if not reunioes:
        st.info("Não há reuniões cadastradas.")
    else:
        opcoes = [
            f"{i} - {r.assunto} | {r.data.strftime('%d/%m/%Y')} {r.horario.strftime('%H:%M')} | Sala {r.sala.numero}"
            for i, r in enumerate(reunioes)
        ]

        reuniao_escolhida = st.selectbox("Selecione a reunião", opcoes)
        indice = int(reuniao_escolhida.split(" - ")[0])
        reuniao = reunioes[indice]

        nova_data = st.date_input("Nova data", value=reuniao.data, key="nova_data")
        novo_horario_str = st.selectbox(
            "Novo horário",
            ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"],
            key="novo_horario"
        )
        nova_sala_numero = st.selectbox(
            "Nova sala",
            [s.numero for s in st.session_state.salas],
            key="nova_sala"
        )

        if st.button("Realocar reunião"):
            nova_sala = next(s for s in st.session_state.salas if s.numero == nova_sala_numero)
            novo_horario = datetime.strptime(novo_horario_str, "%H:%M").time()

            conflito = False
            for i, r in enumerate(reunioes):
                if i != indice and r.sala.numero == nova_sala.numero and r.data == nova_data and r.horario == novo_horario:
                    conflito = True
                    break

            if conflito:
                st.error("A nova sala já está ocupada nesse horário.")
            else:
                reuniao.realocar(nova_sala, nova_data, novo_horario)
                st.success("Reunião realocada com sucesso!")

with tab5:
    st.subheader("Reuniões do dia")

    data_consulta = st.date_input("Escolha a data da agenda", value=agenda.data, key="consulta_data")
    agenda.data = data_consulta

    reunioes_dia = agenda.listar_reunioes()

    if reunioes_dia:
        df_reunioes = pd.DataFrame([r.exibir() for r in reunioes_dia])
        st.dataframe(df_reunioes, use_container_width=True)
    else:
        st.info("Não há reuniões para essa data.")

    st.subheader("Consultar salas livres")

    if st.session_state.salas:
        horario_consulta_str = st.selectbox(
            "Escolha o horário",
            ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"],
            key="consulta_horario"
        )

        if st.button("Ver salas livres"):
            horario_consulta = datetime.strptime(horario_consulta_str, "%H:%M").time()
            livres = agenda.consultar_salas_livres(st.session_state.salas, horario_consulta)

            if livres:
                df_livres = pd.DataFrame([s.exibir() for s in livres])
                st.dataframe(df_livres, use_container_width=True)
            else:
                st.warning("Nenhuma sala livre nesse horário.")
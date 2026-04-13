import pandas as pd
import streamlit as st
from models import Musico, Musica, CD, ColecaoCD

st.set_page_config(page_title="Coleção de CDs", page_icon="💿")
st.title("Coleção de CDs - Variação A")

if "colecao" not in st.session_state:
    st.session_state.colecao = ColecaoCD()

if "musicos" not in st.session_state:
    st.session_state.musicos = []

if "musicas" not in st.session_state:
    st.session_state.musicas = []

colecao = st.session_state.colecao

tab1, tab2, tab3, tab4 = st.tabs([
    "Cadastrar Músico",
    "Cadastrar Música",
    "Cadastrar CD",
    "Consultas"
])

with tab1:
    st.subheader("Cadastrar músico")

    with st.form("form_musico"):
        nome_musico = st.text_input("Nome do músico ou conjunto")
        salvar_musico = st.form_submit_button("Salvar músico")

    if salvar_musico:
        if not nome_musico.strip():
            st.warning("Informe o nome do músico.")
        else:
            existe = any(m.nome.lower() == nome_musico.lower() for m in st.session_state.musicos)
            if existe:
                st.warning("Esse músico já foi cadastrado.")
            else:
                st.session_state.musicos.append(Musico(nome_musico))
                st.success("Músico cadastrado com sucesso!")

    if st.session_state.musicos:
        st.write("Músicos cadastrados:")
        df_musicos = pd.DataFrame([m.exibir() for m in st.session_state.musicos])
        st.dataframe(df_musicos, use_container_width=True)

with tab2:
    st.subheader("Cadastrar música")

    with st.form("form_musica"):
        titulo_musica = st.text_input("Título da música")
        duracao_musica = st.text_input("Duração", placeholder="Ex: 03:45")
        salvar_musica = st.form_submit_button("Salvar música")

    if salvar_musica:
        if not titulo_musica.strip() or not duracao_musica.strip():
            st.warning("Preencha título e duração.")
        else:
            existe = any(m.titulo.lower() == titulo_musica.lower() for m in st.session_state.musicas)
            if existe:
                st.warning("Essa música já foi cadastrada.")
            else:
                st.session_state.musicas.append(Musica(titulo_musica, duracao_musica))
                st.success("Música cadastrada com sucesso!")

    if st.session_state.musicas:
        st.write("Músicas cadastradas:")
        df_musicas = pd.DataFrame([m.exibir() for m in st.session_state.musicas])
        st.dataframe(df_musicas, use_container_width=True)

with tab3:
    st.subheader("Cadastrar CD")

    nomes_musicos = [m.nome for m in st.session_state.musicos]
    titulos_musicas = [m.titulo for m in st.session_state.musicas]

    with st.form("form_cd"):
        titulo_cd = st.text_input("Título do CD")
        ano_cd = st.number_input("Ano de lançamento", min_value=1900, max_value=2100, step=1)
        coletanea_cd = st.checkbox("É coletânea?")
        duplo_cd = st.checkbox("É duplo?")

        musicos_escolhidos = st.multiselect(
            "Selecione os músicos do CD",
            options=nomes_musicos
        )

        musicas_escolhidas = st.multiselect(
            "Selecione as músicas do CD",
            options=titulos_musicas
        )

        salvar_cd = st.form_submit_button("Salvar CD")

    if salvar_cd:
        if not titulo_cd.strip():
            st.warning("Informe o título do CD.")
        elif not musicos_escolhidos:
            st.warning("Selecione pelo menos um músico.")
        elif not musicas_escolhidas:
            st.warning("Selecione pelo menos uma música.")
        else:
            cd = CD(
                titulo=titulo_cd,
                ano_lancamento=int(ano_cd),
                coletanea=coletanea_cd,
                duplo=duplo_cd
            )

            for nome in musicos_escolhidos:
                musico = next((m for m in st.session_state.musicos if m.nome == nome), None)
                if musico:
                    cd.adicionar_musico(musico)

            for titulo in musicas_escolhidas:
                musica = next((m for m in st.session_state.musicas if m.titulo == titulo), None)
                if musica:
                    cd.adicionar_musica(musica)

            colecao.adicionar_cd(cd)
            st.success("CD cadastrado com sucesso!")

    if colecao.cds:
        st.write("CDs cadastrados:")
        df_cds = pd.DataFrame(colecao.listar_cds())
        st.dataframe(df_cds, use_container_width=True)

with tab4:
    st.subheader("Buscar CDs por músico")

    busca_musico = st.text_input("Digite o nome do músico", key="busca_musico")
    if st.button("Buscar CDs por músico"):
        resultados = colecao.buscar_cds_por_musico(busca_musico)
        if resultados:
            df = pd.DataFrame([cd.exibir() for cd in resultados])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Nenhum CD encontrado para esse músico.")

    st.subheader("Buscar CDs por música")

    busca_musica = st.text_input("Digite o título da música", key="busca_musica")
    if st.button("Buscar CDs por música"):
        resultados = colecao.buscar_cds_por_musica(busca_musica)
        if resultados:
            df = pd.DataFrame([cd.exibir() for cd in resultados])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Nenhum CD encontrado para essa música.")
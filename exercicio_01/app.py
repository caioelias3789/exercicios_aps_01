import streamlit as st
import pandas as pd

# Lista para armazenar dados (simples, sem banco)
if "dados" not in st.session_state:
    st.session_state.dados = []

st.title("Controle de Conta de Luz")

# Formulário
st.subheader("Cadastrar nova conta")

data_leitura = st.date_input("Data da leitura")
numero_leitura = st.number_input("Número da leitura", min_value=0)
kw_mes = st.number_input("Consumo do mês (kWh)", min_value=0.0)
valor = st.number_input("Valor da conta (R$)", min_value=0.0)
data_pagamento = st.date_input("Data de pagamento")

if st.button("Adicionar"):
    st.session_state.dados.append({
        "Data Leitura": data_leitura,
        "Leitura": numero_leitura,
        "Consumo": kw_mes,
        "Valor": valor,
        "Pagamento": data_pagamento
    })
    st.success("Conta adicionada com sucesso!")

# Mostrar tabela
if st.session_state.dados:
    df = pd.DataFrame(st.session_state.dados)

    # Converter para datetime (garantia)
    df["Data Leitura"] = pd.to_datetime(df["Data Leitura"])

    # Ordenar por data
    df = df.sort_values("Data Leitura")

    st.subheader("Histórico de Contas")
    st.dataframe(df)

    # Média mensal (mantida)
    media_mensal = df["Consumo"].mean()
    st.write(f"📊 Média mensal: {media_mensal:.2f} kWh")

    # 🔥 Cálculo correto da média diária
    if len(df) > 1:
        df["Dias"] = df["Data Leitura"].diff().dt.days

        # Evita erro na primeira linha (NaN)
        df["Consumo Diário"] = df["Consumo"] / df["Dias"]

        # Remove valores inválidos (primeira linha)
        media_diaria = df["Consumo Diário"].dropna().mean()

        st.write(f"📅 Média diária real: {media_diaria:.2f} kWh/dia")
    else:
        st.warning("Adicione pelo menos 2 registros para calcular média diária real.")

    # Maior consumo
    maior = df.loc[df["Consumo"].idxmax()]
    st.write("🔥 Maior consumo:")
    st.write(maior)

    # Menor consumo
    menor = df.loc[df["Consumo"].idxmin()]
    st.write("❄️ Menor consumo:")
    st.write(menor)
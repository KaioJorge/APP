import streamlit as st
import pandas as pd

# Função para somar múltiplas leituras separadas por vírgula ou espaço
def somar_leitura(leitura_str):
    if not leitura_str.strip():
        return 0.0
    partes = leitura_str.replace(',', ' ').split()
    return sum(float(x) for x in partes)

# Função para calcular créditos utilizados e valor total
def calcular_valor(leitura_inicial_total, leitura_final_total, valor_por_credito):
    creditos_utilizados = leitura_final_total - leitura_inicial_total
    valor_total = creditos_utilizados * valor_por_credito
    return creditos_utilizados, valor_total

# Título do app
st.title("Calculadora de Créditos")

st.markdown("Insira as leituras e o valor do crédito para cada máquina abaixo:")

num_maquinas = 70  # Total de máquinas

# Dicionários para armazenar entradas por máquina
leitura_inicial_inputs = {}
leitura_final_inputs = {}
valor_credito_inputs = {}

# Área de preenchimento dos dados
with st.expander("📋 Preencher dados das máquinas", expanded=False):
    for i in range(1, num_maquinas + 1):
        col1, col2, col3 = st.columns(3)
        with col1:
            leitura_inicial_inputs[i] = st.text_input(f"Máquina {i} - Leitura Inicial", key=f"li_{i}")
        with col2:
            leitura_final_inputs[i] = st.text_input(f"Máquina {i} - Leitura Final", key=f"lf_{i}")
        with col3:
            valor_credito_inputs[i] = st.number_input(f"Máquina {i} - Valor do Crédito", min_value=0.0, step=0.01, format="%.2f", key=f"vc_{i}")

# Botão para calcular os resultados
if st.button("Calcular todos os resultados"):
    resultados = []
    erros = []

    for i in range(1, num_maquinas + 1):
        try:
            leitura_inicial = somar_leitura(leitura_inicial_inputs.get(i, ""))
            leitura_final = somar_leitura(leitura_final_inputs.get(i, ""))
            valor_credito = valor_credito_inputs.get(i, 0.0)

            creditos, total = calcular_valor(leitura_inicial, leitura_final, valor_credito)
            if creditos < 0:
                erros.append(f"Máquina {i}: Leitura final menor que a inicial.")
                creditos = 0
                total = 0

            resultados.append({
                "Máquina": i,
                "Leitura Inicial": leitura_inicial,
                "Leitura Final": leitura_final,
                "Créditos Utilizados": creditos,
                "Valor Crédito (R$)": valor_credito,
                "Valor Total (R$)": total
            })
        except Exception as e:
            erros.append(f"Máquina {i}: Erro no cálculo - {e}")
            resultados.append({
                "Máquina": i,
                "Leitura Inicial": None,
                "Leitura Final": None,
                "Créditos Utilizados": None,
                "Valor Crédito (R$)": valor_credito_inputs.get(i, 0.0),
                "Valor Total (R$)": None
            })

    # Mostra tabela com resultados
    df_resultados = pd.DataFrame(resultados)
    st.subheader("📊 Resultados por Máquina")
    st.dataframe(df_resultados.style.format({
        "Leitura Inicial": "{:.2f}",
        "Leitura Final": "{:.2f}",
        "Créditos Utilizados": "{:.2f}",
        "Valor Crédito (R$)": "R$ {:.2f}",
        "Valor Total (R$)": "R$ {:.2f}",
    }))

    # Mostra erros, se houver
    if erros:
        st.error("⚠️ Foram encontrados alguns problemas:")
        for erro in erros:
            st.write(erro)

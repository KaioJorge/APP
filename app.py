import streamlit as st

def somar_leitura(leitura_str):
    partes = leitura_str.replace(',', ' ').split()
    return sum(float(x) for x in partes)

def calcular_valor(leitura_inicial_total, leitura_final_total, valor_por_credito):
    creditos_utilizados = leitura_final_total - leitura_inicial_total
    valor_total = creditos_utilizados * valor_por_credito
    return creditos_utilizados, valor_total

st.title("🎰 Calculadora de Créditos - Máquina de Cassino")

st.markdown("Insira as leituras e o valor do crédito para calcular quanto foi inserido na máquina.")

leitura_inicial = st.text_input("📥 Leitura inicial (separada por espaço ou vírgula):")
leitura_final = st.text_input("📤 Leitura final (separada por espaço ou vírgula):")
valor_credito = st.number_input("💰 Valor de 1 crédito (R$)", step=0.01)

if st.button("Calcular"):
    try:
        inicial_total = somar_leitura(leitura_inicial)
        final_total = somar_leitura(leitura_final)
        creditos, total = calcular_valor(inicial_total, final_total, valor_credito)

        st.success(f"✅ Leitura Inicial Total: {inicial_total}")
        st.success(f"✅ Leitura Final Total: {final_total}")
        st.success(f"🎯 Créditos Utilizados: {creditos}")
        st.success(f"💸 Valor Total: R$ {total:.2f}")
    except ValueError as e:
        st.error(f"❌ Erro no cálculo: {e}")

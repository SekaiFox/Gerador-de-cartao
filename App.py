#PASSO A PASSO PARA UTILIZAÇÃO
# 1. Instale as bibliotecas:
#    pip install streamlit pandas
# 2. Salve este código (por exemplo, `gerador_cartao_completo.py`).
# 3. Execute o aplicativo:
#    streamlit run gerador_cartao_completo.py
# 4. IMPORTANTE: Estes dados são FALSOS, gerados matematicamente.
#    Use apenas para ambientes de teste e desenvolvimento.

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from io import BytesIO

# --- LISTAS PARA GERAÇÃO DE NOMES ---
LISTA_PRIMEIROS_NOMES = [
    "Marcos", "Ana", "Carlos", "Beatriz", "Pedro", "Juliana", "Rafael", "Lucia",
    "Fernando", "Camila", "Bruno", "Patricia", "Leonardo", "Sofia", "Ricardo"
]
LISTA_SOBRENOMES = [
    "Leon", "Silva", "Souza", "Ferreira", "Santos", "Oliveira", "Pereira",
    "Rodrigues", "Almeida", "Nunes", "Costa", "Gomes", "Martins", "Carvalho"
]
INICIAIS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# --- CONFIGURAÇÕES DE CARTÕES (IIN/BIN) ---
# Chave: Descrição para o Selectbox
# Valor: Dicionário com prefixos, comprimento, bandeira e banco
# Fontes de IINs: [2.2] (BB), [3.5] (Itaú)
CONFIG_CARTOES = {
    # --- Genéricos (Banco Desconhecido) ---
    "Visa (Genérico)": {
        "prefixos": ["4"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Genérico"
    },
    "Mastercard (Genérico)": {
        "prefixos": ["51", "52", "53", "54", "55"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Genérico"
    },
    "American Express (Genérico)": {
        "prefixos": ["34", "37"],
        "comprimento": 15,
        "bandeira": "American Express",
        "banco": "Genérico"
    },
    "Elo (Genérico)": {
        "prefixos": ["636368", "504175", "5067", "509", "627780"],
        "comprimento": 16,
        "bandeira": "Elo",
        "banco": "Genérico"
    },
    
    # --- Específicos (Banco do Brasil - Ourocard) ---
    "Banco do Brasil - Visa Gold (Ourocard)": {
        "prefixos": ["498407"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Banco do Brasil"
    },
    "Banco do Brasil - Visa Infinite (Ourocard)": {
        "prefixos": ["498408"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Banco do Brasil"
    },
    "Banco do Brasil - Mastercard Gold (Ourocard)": {
        "prefixos": ["546452"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Banco do Brasil"
    },
    "Banco do Brasil - Mastercard Black (Ourocard)": {
        "prefixos": ["552289"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Banco do Brasil"
    },
    "Banco do Brasil - Elo Mais (Ourocard)": {
        "prefixos": ["650487"],
        "comprimento": 16,
        "bandeira": "Elo",
        "banco": "Banco do Brasil"
    },
    
    # --- Específico (Itaú Unibanco) ---
    "Itaú Unibanco - Mastercard": {
        "prefixos": ["511258"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Itaú Unibanco"
    }
}


# --- FUNÇÕES DE GERAÇÃO ---

def gerar_nome_ficticio():
    """Gera um nome com inicial do meio, ex: Marcos C. Leon"""
    primeiro = random.choice(LISTA_PRIMEIROS_NOMES)
    sobrenome = random.choice(LISTA_SOBRENOMES)
    inicial = random.choice(INICIAIS)
    return f"{primeiro} {inicial}. {sobrenome}"

def calcular_luhn_dv(base_numero):
    """Calcula o dígito verificador usando o Algoritmo de Luhn (Módulo 10)"""
    pesos = [2, 1]
    soma_produtos = 0
    base_invertida = base_numero[::-1] # Inverte a string
    
    for i, digito_str in enumerate(base_invertida):
        peso = pesos[i % len(pesos)]
        produto = int(digito_str) * peso
        soma_produtos += (produto // 10) + (produto % 10)
        
    resto = soma_produtos % 10
    dv = 0 if resto == 0 else (10 - resto)
    return str(dv)

def gerar_cartao_credito(config_cartao):
    """Gera um conjunto completo de dados de cartão de crédito."""
    
    # 1. Número do Cartão (com Luhn)
    prefixo = random.choice(config_cartao["prefixos"])
    comprimento = config_cartao["comprimento"]
    
    # Gera o "meio" do cartão
    comprimento_meio = comprimento - len(prefixo) - 1 # -1 para o DV
    meio_cartao = ''.join([str(random.randint(0, 9)) for _ in range(comprimento_meio)])
    
    # Base para cálculo do DV
    base_calculo = prefixo + meio_cartao
    dv = calcular_luhn_dv(base_calculo)
    
    numero_cartao = base_calculo + dv
    
    # 2. Nome Fictício
    nome_cartao = gerar_nome_ficticio()
    
    # 3. Data de Validade (MM/AA)
    hoje = datetime.now()
    ano_futuro = hoje.year + random.randint(1, 5)
    mes_futuro = random.randint(1, 12)
    validade = f"{mes_futuro:02d}/{ano_futuro % 100:02d}" # Formato MM/AA
    
    # 4. CVV (Código de Segurança)
    if config_cartao["bandeira"] == "American Express":
        cvv = f"{random.randint(1000, 9999):04d}"
    else:
        cvv = f"{random.randint(0, 999):03d}"
        
    return (
        nome_cartao, 
        config_cartao["banco"], 
        config_cartao["bandeira"], 
        numero_cartao, 
        validade, 
        cvv
    )

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="Gerador de Cartão de Crédito", layout="centered")
st.title("💳 Gerador de Cartões de Crédito (para Testes)")
st.warning("Estes dados são **100% FALSOS** e devem ser usados **APENAS** em ambientes de teste (sandbox).")
st.info("Os IINs (prefixos) de bancos específicos são baseados em dados públicos limitados.")

# Selectbox para a bandeira
opcoes_cartao = list(CONFIG_CARTOES.keys())

# Ordena a lista para melhor visualização (Genéricos primeiro)
opcoes_cartao.sort(key=lambda x: (not x.endswith("(Genérico)"), x))

tipo_cartao_selecionado = st.selectbox(
    "Qual tipo de cartão (Banco/Bandeira) deseja gerar?",
    options=opcoes_cartao
)

# Input para quantidade
quantidade = st.number_input("Quantos cartões deseja gerar?", min_value=1, max_value=1000, value=10)

if st.button("Gerar Cartões"):
    
    # Pega a configuração completa do dicionário
    config_selecionada = CONFIG_CARTOES[tipo_cartao_selecionado]
    
    cartoes_gerados = []
    for _ in range(quantidade):
        cartoes_gerados.append(gerar_cartao_credito(config_selecionada))
    
    # Criar DataFrame
    df = pd.DataFrame(
        cartoes_gerados,
        columns=["Nome no Cartão", "Banco Emissor", "Bandeira", "Número do Cartão", "Validade (MM/AA)", "CVV"]
    )

    st.success(f"{quantidade} cartões '{tipo_cartao_selecionado}' gerados com sucesso!")
    st.dataframe(df)

    # Criar arquivo Excel para download
    output = BytesIO()
    df.to_excel(output, index=False)
    st.download_button(
        label="📥 Baixar Cartões em Excel",
        data=output.getvalue(),
        file_name="cartoes_teste.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
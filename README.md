# 💳 Gerador de Cartões de Crédito para Testes (Sandbox)

Uma aplicação web (Python + Streamlit) que gera dados completos de cartões de crédito **100% fictícios** para uso exclusivo em ambientes de teste e *sandbox* de pagamento.

---
### ⚠️ AVISO EXTREMAMENTE IMPORTANTE
**Este projeto foi desenvolvido para fins acadêmicos e de teste de gateways de pagamento (sandbox).**

Os dados gerados são **100% FALSOS** e aleatórios. Eles **NÃO** são cartões de crédito reais e **NÃO** possuem valor monetário. Eles são matematicamente válidos apenas para passar em validações de formulário.

**Qualquer tentativa de uso desses dados para transações reais é crime (fraude) e de inteira responsabilidade do usuário.**
---

![GeradorDeCartao_tk_BJ9eFInfwJ](https://github.com/user-attachments/assets/120c9f1c-b993-494c-aff7-5e65624877ed)


## 🎯 O Problema (Contexto de Desenvolvimento)

Desenvolvedores que integram APIs de pagamento (Stripe, Mercado Pago, Pagar.me) precisam testar seus *checkouts*. Esses ambientes de *sandbox* exigem números de cartão que passem na primeira camada de validação: o **Algoritmo de Luhn**.

## 💡 A Solução (Habilidade Técnica)

Esta ferramenta gera um conjunto completo de dados de teste (Nome, Número, Validade, CVV). Os números de cartão são sinteticamente válidos pois:

1.  **Implementam o Algoritmo de Luhn (Módulo 10):** O algoritmo padrão da indústria para validar o dígito verificador do cartão.
2.  **Usam IIN/BIN Corretos:** Os prefixos (primeiros 6 dígitos) correspondem a bancos e bandeiras reais (ex: `4984...` para BB Visa, `5112...` para Itaú Master), permitindo testar lógicas de sistema baseadas no tipo de cartão.
3.  **Gera Dados Coerentes:** Cria nomes fictícios, datas de validade futuras e CVVs aleatórios.

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Streamlit**
* **Pandas** (para exportação para Excel)

## 🏁 Como Executar o Projeto

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SekaiFox/Gerador-de-cartao.git](https://github.com/SekaiFox/Gerador-de-cartao.git)
    cd Gerador-de-cartao
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  Instale as dependências (crie um arquivo `requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o app Streamlit:
    ```bash
    streamlit run gerador_cartao_credito.py
    ```

**Arquivo `requirements.txt`:**

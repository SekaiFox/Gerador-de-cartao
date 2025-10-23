# Como gerar o .exe (Windows)

Este repositório contém um aplicativo Streamlit (`App.py`) que gera cartões de teste.
Abaixo estão os passos para criar um executável único (.exe) usando o PyInstaller.

Pré-requisitos
- Python 3.8+ instalado
- PowerShell (Windows)

Passos
1. Abra o PowerShell na pasta do projeto.
2. (Opcional) Crie e ative um ambiente virtual:

   python -m venv .venv; .\.venv\Scripts\Activate.ps1

3. Instale dependências:

   pip install -r requirements.txt

4. Rode o script de build:

   ./build_exe.ps1

5. Após o término, o executável estará em `dist\GeradorDeCartao.exe`.

Nota sobre Streamlit
- Streamlit é uma aplicação web. O executável gerado envolverá o script Streamlit.
  Ao executar o .exe, ele irá iniciar o servidor local do Streamlit e abrir a interface no navegador.

Problemas comuns
- Erro de import: verifique se todas as dependências estão listadas em `requirements.txt`.
- Antivírus pode bloquear o executável gerado — marque como confiável ou adicione exceção.

Se quiser, eu posso rodar o build aqui (se você permitir que eu instale dependências e execute comandos).
# Script PowerShell para gerar .exe usando PyInstaller
# Uso: Execute no PowerShell na raiz do projeto
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#   pip install -r requirements.txt
#   ./build_exe.ps1

$mainScript = "App.py"
$distName = "GeradorDeCartao"
$iconPath = "" # Se você tiver um .ico, informe o caminho aqui

# Opções recomendadas:
# --onefile : cria um único executável
# --noconsole : esconde o console (não recomendado para debug)
# --add-data : incluir arquivos extras (formato: "source;dest" no Windows)

$addData = ""
# Exemplo para incluir um ícone ou outros assets:
# $addData = "assets\logo.png;assets"

$iconArg = ""
if ($iconPath -ne "") {
    $iconArg = "--icon=$iconPath"
}

# Comando PyInstaller
$cmd = "pyinstaller --onefile $iconArg --name $distName $addData $mainScript"
Write-Host "Executando: $cmd"
Invoke-Expression $cmd

Write-Host "Build finalizado. Verifique a pasta 'dist' para o executável."
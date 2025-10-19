@echo off
chcp 65001 > nul
color 0B
title 🚀 SITE PROFISSIONAL LUDURANO - INICIALIZADOR

echo.
echo ======================================================================
echo 🚀 SITE PROFISSIONAL LUDURANO - FLASK VERSION
echo ======================================================================
echo.

REM Verificar se Python está instalado
echo [1/4] 🔍 Verificando instalação do Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.13+ em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python encontrado!
python --version
echo.

REM Verificar se as dependências estão instaladas
echo [2/4] 📦 Verificando dependências...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dependências não instaladas. Instalando agora...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERRO ao instalar dependências!
        echo.
        pause
        exit /b 1
    )
    echo ✅ Dependências instaladas com sucesso!
) else (
    echo ✅ Dependências OK!
)
echo.

REM Parar processos Python antigos
echo [3/4] 🔄 Parando servidores antigos...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo ✅ Servidores antigos encerrados!
echo.

REM Iniciar o servidor
echo [4/4] 🚀 Iniciando servidor Flask...
echo.
echo ======================================================================
echo 🌐 ACESSO AO SITE:
echo ======================================================================
echo.
echo 📱 PÚBLICO:  http://127.0.0.1:5000
echo 🔐 ADMIN:    http://127.0.0.1:5000/ceo-login-ultra-secreto-2025
echo.
echo 👤 Usuário:  CEO
echo 🔑 Senha:    CEO2025@Premium
echo.
echo ======================================================================
echo.
echo ⚡ Pressione CTRL+C para parar o servidor
echo.
echo ======================================================================
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo ❌ ERRO AO INICIAR O SERVIDOR!
    echo ======================================================================
    echo.
    echo Possíveis soluções:
    echo 1. Verifique se a porta 5000 está livre
    echo 2. Execute: pip install -r requirements.txt --upgrade
    echo 3. Verifique se o arquivo app.py existe
    echo.
    pause
    exit /b 1
)

pause

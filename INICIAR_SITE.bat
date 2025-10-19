@echo off
chcp 65001 > nul
color 0B
title 🚀 SITE OFICIAL - INICIANDO SERVIDOR

echo.
echo ======================================================================
echo 🚀 INICIANDO SEU SITE OFICIAL - TYPESCRIPT/REACT
echo ======================================================================
echo.

cd "C:\Users\User\Luduranoficiall-TypeScript"

echo [1/2] 🔄 Parando servidores antigos...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo ✅ Servidores antigos encerrados!
echo.

echo [2/2] 🚀 Iniciando servidor de desenvolvimento...
echo.
echo ======================================================================
echo 🌐 SEU SITE ESTARÁ DISPONÍVEL EM:
echo ======================================================================
echo.
echo 📱 LOCAL:    http://localhost:5173
echo 🌍 REDE:     http://[seu-ip]:5173
echo.
echo ⚡ Pressione CTRL+C para parar o servidor
echo.
echo ======================================================================
echo.

npm run dev

pause

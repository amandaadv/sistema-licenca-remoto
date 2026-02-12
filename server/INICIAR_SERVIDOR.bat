@echo off
chcp 65001 >nul
title SERVIDOR DE LICENÇAS - ZAPJOE V2

echo.
echo ======================================================================
echo           SERVIDOR DE LICENÇAS - ZAPJOE V2
echo ======================================================================
echo.

cd /d "%~dp0"

echo [!] Verificando se servidor já está rodando...
tasklist | findstr /i "python.exe.*api.py" >nul
if %errorlevel%==0 (
    echo [OK] Servidor já está rodando!
    echo.
    goto :show_info
)

echo [->] Iniciando servidor...
echo.

start /B python api.py

timeout /t 3 /nobreak >nul

:show_info
echo ======================================================================
echo           SERVIDOR ONLINE
echo ======================================================================
echo.

:: Pegar IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)

:found_ip
set IP=%IP: =%

echo [Net] URL Local (mesmo PC):
echo      http://localhost:8000
echo.
echo [Net] URL Rede (outros PCs na rede):
echo      http://%IP%:8000
echo.
echo [!] Para acessar de OUTRO PC:
echo     1. Copie o programa para o outro PC
echo     2. Edite: config\servidor_licenca.json
echo     3. Troque para: http://%IP%:8000
echo.
echo [!] Para acessar de QUALQUER LUGAR (internet):
echo     - Use um serviço como ngrok, Heroku, ou DigitalOcean
echo.
echo ======================================================================
echo.
echo [Key] Pressione qualquer tecla para voltar...
pause >nul

@echo off
chcp 65001 >nul
title DEPLOY AUTOMÁTICO - RAILWAY

echo.
echo ======================================================================
echo           DEPLOY AUTOMÁTICO - RAILWAY
echo ======================================================================
echo.

cd /d "%~dp0"

:: Verificar se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Git não está instalado!
    echo.
    echo Baixe em: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [!] Este script vai fazer o deploy do servidor no Railway
echo.
echo VOCÊ PRECISA TER:
echo   1. Conta no Railway (railway.app)
echo   2. Conta no GitHub (github.com)
echo   3. Repositório criado no GitHub
echo.

set /p CONTINUAR="Continuar? (s/n): "
if /i not "%CONTINUAR%"=="s" exit /b 0

echo.
echo ======================================================================
echo           CONFIGURAÇÃO
echo ======================================================================
echo.

:: Pedir URL do repositório
set /p REPO_URL="Cole a URL do seu repositório GitHub: "
if "%REPO_URL%"=="" (
    echo [X] URL não pode estar vazia!
    pause
    exit /b 1
)

echo.
echo [->] Verificando se já é um repositório Git...

if exist ".git" (
    echo [OK] Já é um repositório Git
    echo.
    set /p UPDATE="Fazer update (push)? (s/n): "
    if /i "%UPDATE%"=="s" (
        goto :do_push
    ) else (
        exit /b 0
    )
)

echo [!] Primeiro deploy - Inicializando...
echo.

:: Inicializar Git
git init

:: Adicionar arquivos
echo [->] Adicionando arquivos...
git add .

:: Commit
echo [->] Criando commit...
git commit -m "Initial commit - ZAPJOE License Server"

:: Adicionar remote
echo [->] Conectando com GitHub...
git remote add origin %REPO_URL%

:: Push
:do_push
echo [->] Enviando código para GitHub...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [X] Erro ao fazer push!
    echo.
    echo Possíveis causas:
    echo   1. URL do repositório incorreta
    echo   2. Não está autenticado no Git
    echo   3. Repositório não existe
    echo.
    echo Para autenticar, use Personal Access Token:
    echo https://github.com/settings/tokens
    echo.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo           SUCESSO!
echo ======================================================================
echo.
echo [OK] Código enviado para GitHub com sucesso!
echo.
echo PRÓXIMOS PASSOS:
echo.
echo 1. Acesse: https://railway.app/dashboard
echo 2. Clique em "New Project"
echo 3. Selecione "Deploy from GitHub repo"
echo 4. Escolha seu repositório
echo 5. Aguarde o deploy (2-3 minutos)
echo 6. Copie a URL gerada
echo 7. Configure no cliente: config\servidor_licenca.json
echo.
echo ======================================================================
echo.
pause

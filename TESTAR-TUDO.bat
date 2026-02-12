@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║          SISTEMA DE LICENÇAS REMOTO - TESTE COMPLETO        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo     ❌ Python não instalado! Instale Python 3.8+
    pause
    exit /b 1
)
echo     ✅ Python instalado
echo.

echo [2/5] Instalando dependências...
pip install fastapi uvicorn requests pydantic >nul 2>&1
if errorlevel 1 (
    echo     ❌ Erro ao instalar dependências
    pause
    exit /b 1
)
echo     ✅ Dependências instaladas
echo.

echo [3/5] Iniciando servidor (aguarde 5 segundos)...
start "ZAPJOE Licenses Server" cmd /k "cd server && python api.py"
timeout /t 5 /nobreak >nul
echo     ✅ Servidor iniciado
echo.

echo [4/5] Abrindo painel admin...
start "ZAPJOE Admin Panel" cmd /k "cd admin && python painel_admin.py"
echo     ✅ Painel admin aberto
echo.

echo [5/5] Teste completo!
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                      TESTE INICIADO!                         ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo PRÓXIMOS PASSOS:
echo.
echo 1. No PAINEL ADMIN, escolha: 2. Adicionar novo cliente
echo    - Usuário: teste
echo    - Senha: 123456
echo    - Validade: 2 (30 dias)
echo.
echo 2. Depois, teste o cliente:
echo    cd cliente
echo    python licenca_client.py
echo.
echo 3. Use usuário: teste / senha: 123456
echo.
echo 4. Se aparecer "✅ Licença válida" = SUCESSO!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

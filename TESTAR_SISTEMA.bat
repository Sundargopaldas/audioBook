@echo off
echo ===========================================
echo TESTANDO SISTEMA DE NARRACAO
echo ===========================================
echo.

echo Verificando servidor de arquivos (porta 8080)...
curl -s http://localhost:8080/testar_narracao_porta_8001.html > nul
if %errorlevel% == 0 (
    echo [OK] Servidor de arquivos funcionando!
) else (
    echo [ERRO] Servidor de arquivos NAO esta rodando!
)

echo.
echo Verificando backend API (porta 8001)...
curl -s http://localhost:8001/docs > nul
if %errorlevel% == 0 (
    echo [OK] Backend API funcionando!
) else (
    echo [ERRO] Backend API NAO esta rodando!
)

echo.
echo ===========================================
echo.
echo Para iniciar o sistema completo, execute:
echo INICIAR_SERVIDOR_E_BACKEND.bat
echo.
pause 
@echo off
echo =====================================================
echo    INICIANDO SISTEMA COMPLETO DE AUDIOBOOK
echo =====================================================
echo.

echo [1/3] Iniciando Backend API na porta 8001...
cd /d "%~dp0"
start "Backend Audiobook" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8001"

echo [2/3] Aguardando backend iniciar...
timeout /t 8 /nobreak > nul

echo [3/3] Iniciando Frontend React...
start "Frontend React" cmd /k "cd frontend && npm start"

echo.
echo =====================================================
echo    SISTEMA INICIADO COM SUCESSO!
echo =====================================================
echo.
echo Backend API: http://localhost:8001
echo Frontend React: http://localhost:3000 (aguarde abrir)
echo Pagina de Teste: http://localhost:8001/testar_sistema_melhorado.html
echo.
echo IMPORTANTE: Aguarde o navegador abrir automaticamente
echo.
echo Para parar os servicos: Feche as janelas do terminal
echo.
pause 
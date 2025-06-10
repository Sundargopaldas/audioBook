@echo off
echo ===========================================
echo INICIANDO SISTEMA DE NARRACAO COM TTS
echo ===========================================
echo.

echo Fechando processos Python anteriores...
taskkill /F /IM python.exe 2>nul

echo.
echo Aguardando...
timeout /t 2 /nobreak >nul

echo.
echo Iniciando servidor de arquivos estaticos (porta 8080)...
start /B cmd /c "cd /d C:\Users\HP\Desktop\Nova pasta && python servidor_simples.py"

echo.
echo Aguardando servidor iniciar...
timeout /t 3 /nobreak >nul

echo.
echo Iniciando backend API (porta 8001)...
cd /d "C:\Users\HP\Desktop\Nova pasta\backend"
start /B cmd /c "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"

echo.
echo Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

echo.
echo ===========================================
echo SISTEMA INICIADO!
echo ===========================================
echo.
echo Servidor de arquivos: http://localhost:8080
echo Backend API: http://localhost:8001
echo.
echo Abrindo pagina de teste...
start http://localhost:8080/testar_narracao_porta_8001.html

echo.
echo Pressione qualquer tecla para fechar todos os servicos...
pause >nul

echo.
echo Fechando servicos...
taskkill /F /IM python.exe
echo.
pause 
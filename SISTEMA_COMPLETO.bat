@echo off
echo ===========================================
echo SISTEMA DE AUDIOBOOK COM IA - GOOGLE TTS
echo ===========================================
echo.

echo Fechando processos anteriores...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul

echo.
echo Aguardando...
timeout /t 2 /nobreak >nul

echo.
echo [1/3] Iniciando Backend API (porta 8001)...
cd /d "C:\Users\HP\Desktop\Nova pasta\backend"
start "Backend API" cmd /c "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"

echo.
echo Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] Iniciando Frontend React (porta 3000)...
cd /d "C:\Users\HP\Desktop\Nova pasta\frontend"
start "Frontend React" cmd /c "npm start"

echo.
echo Aguardando frontend compilar...
timeout /t 10 /nobreak >nul

echo.
echo ===========================================
echo SISTEMA INICIADO COM SUCESSO!
echo ===========================================
echo.
echo Backend API:  http://localhost:8001
echo Frontend:     http://localhost:3000
echo.
echo Recursos disponiveis:
echo - Upload de arquivos TXT, PDF e DOCX
echo - Conversao para audio com Google Cloud TTS
echo - Voz de alta qualidade em portugues (pt-BR-Chirp3-HD-Achernar)
echo.
echo O navegador sera aberto automaticamente...
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo Pressione qualquer tecla para PARAR todos os servicos...
pause >nul

echo.
echo Encerrando servicos...
taskkill /F /IM node.exe
taskkill /F /IM python.exe
echo.
echo Sistema encerrado.
pause 
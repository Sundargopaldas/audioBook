@echo off
echo =====================================================
echo    INICIANDO PROJETO AUDIOBOOK AI COM NARRACAO
echo =====================================================
echo.

echo [1/4] Fechando processos antigos...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak > nul

echo [2/4] Iniciando Backend API...
cd /d "%~dp0backend"
start "Backend API" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak > nul

echo [3/4] Verificando se o backend esta rodando...
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Backend nao iniciou corretamente!
    pause
    exit /b 1
)
echo Backend OK!

echo [4/4] Iniciando Frontend...
cd /d "%~dp0frontend"
start "Frontend React" cmd /k "npm start"

echo.
echo =====================================================
echo    TODOS OS SERVICOS FORAM INICIADOS!
echo =====================================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000 (aguarde abrir)
echo Documentacao API: http://localhost:8000/docs
echo.
echo IMPORTANTE: O sistema agora usa Google Cloud TTS
echo para gerar narracao em portugues!
echo.
echo Para testar:
echo 1. Aguarde o navegador abrir (pode levar 30 segundos)
echo 2. Faca upload de um arquivo TXT, PDF ou DOCX
echo 3. A narracao sera gerada com voz de alta qualidade
echo.
echo Pressione CTRL+C nas janelas para parar os servicos
echo.
pause 
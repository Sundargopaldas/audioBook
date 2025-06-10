@echo off
echo ===========================================
echo    INICIANDO PROJETO AUDIOBOOK COM IA
echo ===========================================
echo.

echo [1/3] Iniciando Backend API...
cd backend
start cmd /k "python -m uvicorn app.main:app --reload"
timeout /t 5 /nobreak > nul

echo [2/3] Iniciando Celery Worker...
start cmd /k "celery -A app.core.celery_app worker --loglevel=info --pool=solo"
timeout /t 3 /nobreak > nul

echo [3/3] Iniciando Frontend...
cd ..\frontend
start cmd /k "npm start"

echo.
echo ===========================================
echo    TODOS OS SERVICOS FORAM INICIADOS!
echo ===========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Aguarde alguns segundos para tudo carregar...
echo.
pause 
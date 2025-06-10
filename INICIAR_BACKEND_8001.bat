@echo off
echo Fechando processos Python anteriores...
taskkill /F /IM python.exe 2>nul

echo.
echo Mudando para o diretorio do projeto...
cd /d "C:\Users\HP\Desktop\Nova pasta"

echo.
echo Iniciando backend na porta 8001...
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
pause 
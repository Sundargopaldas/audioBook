@echo off
echo ==================================================
echo    SISTEMA DE AUDIOBOOK - INICIANDO SERVIDOR
echo ==================================================
echo.

REM Navegar para o diretório backend
cd /d "%~dp0backend"

REM Verificar se estamos no diretório correto
if not exist "app\main.py" (
    echo ERRO: Não foi possível encontrar o arquivo app\main.py
    echo Verifique se você está no diretório correto.
    pause
    exit /b 1
)

echo Diretório atual: %CD%
echo.

REM Ativar ambiente virtual se existir
if exist "..\venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call ..\venv\Scripts\activate.bat
)

echo.
echo Iniciando servidor FastAPI na porta 8001...
echo.
echo Aguarde o servidor iniciar e então acesse:
echo.
echo    http://localhost:8001/testar_sistema_melhorado.html
echo.
echo ==================================================
echo.

REM Iniciar o servidor
python -m uvicorn app.main:app --reload --port 8001

pause 
@echo off
echo ==================================================
echo          INICIANDO SERVIDOR BACKEND
echo ==================================================
echo.

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else if exist ..\venv\Scripts\activate.bat (
    echo Ativando ambiente virtual do diretório pai...
    call ..\venv\Scripts\activate.bat
)

echo.
echo Iniciando servidor FastAPI na porta 8001...
echo.
echo URLs disponíveis após inicialização:
echo - API: http://localhost:8001
echo - Documentação: http://localhost:8001/docs
echo - Painel: http://localhost:8001/testar_sistema_melhorado.html
echo.
echo Pressione CTRL+C para parar o servidor
echo.

python -m uvicorn app.main:app --reload --port 8001 
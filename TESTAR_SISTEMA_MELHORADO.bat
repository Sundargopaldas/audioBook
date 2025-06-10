@echo off
echo ==================================================
echo        SISTEMA DE AUDIOBOOK - TESTE MELHORADO
echo ==================================================
echo.

REM Criar diretórios necessários
echo [1/4] Criando diretórios necessários...
mkdir uploads 2>nul
mkdir audiofiles 2>nul
mkdir backend\uploads 2>nul
mkdir backend\audiofiles 2>nul
echo ✓ Diretórios criados

REM Atualizar banco de dados
echo.
echo [2/4] Atualizando banco de dados...
cd backend
python atualizar_banco.py
cd ..

REM Iniciar backend
echo.
echo [3/4] Iniciando backend na porta 8001...
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8001"

REM Aguardar backend iniciar
echo.
echo [4/4] Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

REM Abrir página de teste
echo.
echo ✓ Abrindo página de teste melhorada...
start http://localhost:8001/testar_sistema_melhorado.html

REM Mostrar informações
echo.
echo ==================================================
echo              SISTEMA INICIADO COM SUCESSO!
echo ==================================================
echo.
echo Funcionalidades disponíveis:
echo - Upload de arquivos TXT, PDF e DOCX
echo - Conversão para áudio com Google TTS
echo - Adição automática de música de fundo
echo - Visualização de todos os arquivos salvos
echo - Painel de controle completo
echo.
echo URLs disponíveis:
echo - Backend API: http://localhost:8001
echo - Documentação: http://localhost:8001/docs
echo - Painel de Controle: http://localhost:8001/testar_sistema_melhorado.html
echo.
echo Pressione CTRL+C no terminal do backend para parar o servidor
echo.
pause 
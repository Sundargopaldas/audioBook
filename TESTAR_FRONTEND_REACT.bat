@echo off
echo ========================================
echo TESTE DO SISTEMA REACT COMPLETO
echo ========================================
echo.

echo 1. Abrindo o frontend React...
start http://localhost:3000

echo.
echo 2. O backend deve estar rodando em: http://localhost:8001
echo 3. Servidor de arquivos estaticos em: http://localhost:8080
echo.
echo INSTRUCOES DE TESTE:
echo - Clique em "Escolher arquivo" no site React
echo - Selecione um arquivo PDF, DOCX ou TXT
echo - Aguarde o processamento
echo - O audio deve tocar automaticamente quando pronto
echo.
echo Se houver problemas, verifique o console do navegador (F12)
echo.
pause 
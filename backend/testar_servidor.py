"""
Script para testar o servidor FastAPI
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    print("✓ Módulo app importado com sucesso!")
    
    # Testar se consegue acessar as rotas
    from app.api.v1.api import api_router
    print("✓ Rotas da API carregadas!")
    
    # Iniciar servidor
    import uvicorn
    print("\nIniciando servidor na porta 8001...")
    print("Acesse: http://localhost:8001/testar_sistema_melhorado.html")
    print("\nPressione CTRL+C para parar o servidor\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
    
except ImportError as e:
    print(f"✗ Erro ao importar módulos: {e}")
    print("\nVerifique se você está no diretório 'backend' e se o ambiente virtual está ativado.")
except Exception as e:
    print(f"✗ Erro: {e}") 
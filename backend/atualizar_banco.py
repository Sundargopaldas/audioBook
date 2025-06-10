"""
Script para atualizar o banco de dados com novos campos
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def column_exists(engine, table_name, column_name):
    """Verifica se uma coluna existe na tabela"""
    inspector = inspect(engine)
    columns = [column['name'] for column in inspector.get_columns(table_name)]
    return column_name in columns

def update_database():
    """Adiciona novos campos à tabela audiobook"""
    
    # Conectar ao banco
    engine = create_engine(settings.DATABASE_URL)
    
    print("Verificando e atualizando banco de dados...")
    
    # Lista de colunas para adicionar
    columns_to_add = [
        ("text_content", "TEXT"),
        ("file_path", "VARCHAR(500)"),
        ("original_file_path", "VARCHAR(500)"),
        ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ("updated_at", "TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP")
    ]
    
    # Verificar e adicionar cada coluna
    with engine.connect() as conn:
        for column_name, column_type in columns_to_add:
            try:
                # Verificar se a coluna já existe
                if column_exists(engine, 'audiobook', column_name):
                    print(f"✓ Coluna '{column_name}' já existe")
                else:
                    # Adicionar a coluna
                    query = f"ALTER TABLE audiobook ADD COLUMN {column_name} {column_type}"
                    conn.execute(text(query))
                    conn.commit()
                    print(f"✓ Coluna '{column_name}' adicionada com sucesso")
            except Exception as e:
                print(f"✗ Erro ao processar coluna '{column_name}': {e}")
                # Tentar continuar com as outras colunas
    
    print("\n✓ Processo de atualização concluído!")
    print("  Colunas verificadas/adicionadas:")
    print("  - text_content: armazena parte do texto extraído")
    print("  - file_path: caminho do arquivo de áudio")
    print("  - original_file_path: caminho do arquivo original")
    print("  - created_at/updated_at: timestamps")

if __name__ == "__main__":
    update_database() 
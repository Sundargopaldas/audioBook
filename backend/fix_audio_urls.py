"""
Script para corrigir as URLs dos audiobooks no banco de dados
"""
import os
import sys

# Adicionar o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.audiobook import Audiobook

def fix_audio_urls():
    db = SessionLocal()
    
    try:
        # Buscar todos os audiobooks
        audiobooks = db.query(Audiobook).all()
        
        for audiobook in audiobooks:
            if audiobook.audio_url:
                # Extrair apenas o nome do arquivo
                filename = audiobook.audio_url.split('/')[-1]
                
                # Atualizar para o novo formato
                if not audiobook.audio_url.startswith('http://localhost:8001/audiofiles/'):
                    new_url = f'http://localhost:8001/audiofiles/{filename}'
                    audiobook.audio_url = new_url
                    print(f"Atualizando audiobook {audiobook.id}: {filename} -> {new_url}")
        
        # Commit das mudanças
        db.commit()
        print("URLs atualizadas com sucesso!")
        
    except Exception as e:
        print(f"Erro ao atualizar URLs: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_audio_urls() 
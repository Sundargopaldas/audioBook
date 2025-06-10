from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.deps import get_db  # Removido get_current_user
from app.schemas.audiobook import AudiobookCreate, AudiobookResponse, AudiobookStatus
from app.crud.audiobooks import audiobooks
from app.tasks.audiobook import process_audiobook, extract_text, convert_text_to_speech, upload_to_s3, add_background_music
from app.models.user import User
import tempfile
import boto3
from app.core.config import settings
import os
import shutil
from datetime import datetime
import hashlib

router = APIRouter()

# Diretórios para armazenamento permanente
# Usar caminhos absolutos para garantir que os arquivos sejam salvos no local correto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
AUDIO_DIR = os.path.join(BASE_DIR, "audiofiles")

# Criar diretórios se não existirem
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

def save_upload_file(file_content: bytes, filename: str) -> str:
    """
    Salva o arquivo enviado permanentemente.
    
    Args:
        file_content: Conteúdo do arquivo
        filename: Nome original do arquivo
        
    Returns:
        Caminho do arquivo salvo
    """
    # Gerar nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_hash = hashlib.md5(file_content).hexdigest()[:8]
    safe_filename = f"{timestamp}_{file_hash}_{filename}"
    
    # Salvar arquivo
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    print(f"[DEBUG] Arquivo original salvo em: {file_path}")
    return file_path

@router.post("/", response_model=AudiobookResponse)
async def create_audiobook(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    """
    Cria um novo audiobook a partir de um arquivo de texto.
    SEM AUTENTICAÇÃO - para teste
    """
    print("[DEBUG] ====== INICIANDO PROCESSAMENTO DE AUDIOBOOK ======")
    print(f"[DEBUG] Nome do arquivo: {file.filename}")
    print(f"[DEBUG] Tipo do arquivo: {file.content_type}")
    
    # Usar usuário padrão (sem autenticação)
    test_user_id = 1
    
    # Validar tipo do arquivo
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de arquivo não suportado. Tipo recebido: {file.content_type}"
        )
    
    # Ler conteúdo do arquivo
    file_content = await file.read()
    print(f"[DEBUG] Tamanho do arquivo: {len(file_content)} bytes")
    
    # Salvar arquivo original permanentemente
    uploaded_file_path = save_upload_file(file_content, file.filename)
    
    # Criar registro do audiobook
    audiobook_data = AudiobookCreate(
        title=file.filename,
        status="processing",
        user_id=test_user_id
    )
    db_audiobook = audiobooks.create(db, obj_in=audiobook_data)
    print(f"[DEBUG] Audiobook criado com ID: {db_audiobook.id}")
    
    # PROCESSAMENTO SÍNCRONO PARA TESTE
    try:
        print("[DEBUG] Extraindo texto do arquivo...")
        # Extrair texto
        text = extract_text(file_content, file.content_type)
        if not text or len(text.strip()) == 0:
            raise ValueError("Não foi possível extrair texto do arquivo")
        
        print(f"[DEBUG] Texto extraído com sucesso. Tamanho: {len(text)} caracteres")
        print(f"[DEBUG] Primeiros 200 caracteres: {text[:200]}...")
        
        # Salvar texto extraído para referência
        text_file_path = os.path.join(UPLOAD_DIR, f"{db_audiobook.id}_texto.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[DEBUG] Texto salvo em: {text_file_path}")
        
        # Gerar narração
        print("[DEBUG] Gerando narração com Google TTS...")
        temp_narration_path = tempfile.mktemp(suffix='.mp3')
        
        # Criar um objeto dummy para a função
        class DummySelf:
            pass
        
        narration_path = convert_text_to_speech(DummySelf(), text, temp_narration_path)
        print(f"[DEBUG] Narração gerada em: {narration_path}")
        
        # Verificar se o arquivo de narração existe
        if not os.path.exists(narration_path):
            raise ValueError(f"Arquivo de narração não foi criado: {narration_path}")
        
        narration_size = os.path.getsize(narration_path)
        print(f"[DEBUG] Tamanho da narração: {narration_size} bytes")
        
        # Adicionar música de fundo
        print("[DEBUG] Adicionando música de fundo...")
        final_audio_path = add_background_music(narration_path)
        print(f"[DEBUG] Áudio final com música: {final_audio_path}")
        
        # Verificar se o arquivo final existe
        if not os.path.exists(final_audio_path):
            print("[AVISO] Usando narração sem música de fundo")
            final_audio_path = narration_path
        
        # Salvar arquivo permanentemente
        final_filename = f"{db_audiobook.id}_audiobook_completo.mp3"
        permanent_path = os.path.join(AUDIO_DIR, final_filename)
        
        print(f"[DEBUG] Copiando arquivo final para: {permanent_path}")
        shutil.copy2(final_audio_path, permanent_path)
        
        # Verificar se o arquivo foi salvo
        if os.path.exists(permanent_path):
            final_size = os.path.getsize(permanent_path)
            print(f"[DEBUG] Arquivo salvo com sucesso! Tamanho: {final_size} bytes")
        else:
            raise ValueError(f"Falha ao salvar arquivo em: {permanent_path}")
        
        # URL para acessar o arquivo
        audio_url = f"http://localhost:8001/audiofiles/{final_filename}"
        
        # Atualizar registro no banco
        update_data = {
            "status": "completed",
            "audio_url": audio_url,
            "progress": 100,
            "current_step": 5,
            "text_content": text[:1000],  # Salvar primeiros 1000 caracteres
            "file_path": permanent_path,
            "original_file_path": uploaded_file_path
        }
        
        audiobooks.update(db, db_obj=db_audiobook, obj_in=update_data)
        
        print(f"[DEBUG] ====== PROCESSAMENTO CONCLUÍDO ======")
        print(f"[DEBUG] URL do áudio: {audio_url}")
        print(f"[DEBUG] Arquivo salvo em: {permanent_path}")
        
        # Limpar apenas arquivos temporários
        try:
            if os.path.exists(temp_narration_path) and temp_narration_path != permanent_path:
                os.remove(temp_narration_path)
            if final_audio_path != narration_path and os.path.exists(final_audio_path) and final_audio_path != permanent_path:
                os.remove(final_audio_path)
        except Exception as e:
            print(f"[AVISO] Erro ao limpar arquivos temporários: {e}")
        
    except Exception as e:
        print(f"[ERRO] Falha no processamento: {str(e)}")
        import traceback
        traceback.print_exc()
        
        audiobooks.update(
            db,
            db_obj=db_audiobook,
            obj_in={
                "status": "error",
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar audiobook: {str(e)}"
        )
    
    return db_audiobook

@router.post("/from-text", response_model=AudiobookResponse)
async def create_audiobook_from_text(
    *,
    db: Session = Depends(get_db),
    title: str = Form(...),
    text: str = Form(...),
):
    """
    Cria um novo audiobook a partir de texto direto.
    """
    print("[DEBUG] ====== INICIANDO PROCESSAMENTO DE AUDIOBOOK (TEXTO DIRETO) ======")
    print(f"[DEBUG] Título: {title}")
    print(f"[DEBUG] Tamanho do texto: {len(text)} caracteres")
    
    # Usar usuário padrão (sem autenticação)
    test_user_id = 1
    
    # Validar texto
    if not text or len(text.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Texto não pode estar vazio"
        )
    
    if len(text.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Texto muito curto. Mínimo de 10 caracteres."
        )
    
    # Criar registro do audiobook
    audiobook_data = AudiobookCreate(
        title=title,
        status="processing",
        user_id=test_user_id
    )
    db_audiobook = audiobooks.create(db, obj_in=audiobook_data)
    print(f"[DEBUG] Audiobook criado com ID: {db_audiobook.id}")
    
    # PROCESSAMENTO SÍNCRONO
    try:
        print(f"[DEBUG] Texto recebido: {text[:200]}...")
        
        # Salvar texto para referência
        text_file_path = os.path.join(UPLOAD_DIR, f"{db_audiobook.id}_texto_direto.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[DEBUG] Texto salvo em: {text_file_path}")
        
        # Gerar narração
        print("[DEBUG] Gerando narração com Google TTS...")
        temp_narration_path = tempfile.mktemp(suffix='.mp3')
        
        # Criar um objeto dummy para a função
        class DummySelf:
            pass
        
        narration_path = convert_text_to_speech(DummySelf(), text, temp_narration_path)
        print(f"[DEBUG] Narração gerada em: {narration_path}")
        
        # Verificar se o arquivo de narração existe
        if not os.path.exists(narration_path):
            raise ValueError(f"Arquivo de narração não foi criado: {narration_path}")
        
        narration_size = os.path.getsize(narration_path)
        print(f"[DEBUG] Tamanho da narração: {narration_size} bytes")
        
        # Adicionar música de fundo
        print("[DEBUG] Adicionando música de fundo...")
        final_audio_path = add_background_music(narration_path)
        print(f"[DEBUG] Áudio final com música: {final_audio_path}")
        
        # Verificar se o arquivo final existe
        if not os.path.exists(final_audio_path):
            print("[AVISO] Usando narração sem música de fundo")
            final_audio_path = narration_path
        
        # Salvar arquivo permanentemente
        final_filename = f"{db_audiobook.id}_audiobook_completo.mp3"
        permanent_path = os.path.join(AUDIO_DIR, final_filename)
        
        print(f"[DEBUG] Copiando arquivo final para: {permanent_path}")
        shutil.copy2(final_audio_path, permanent_path)
        
        # Verificar se o arquivo foi salvo
        if os.path.exists(permanent_path):
            final_size = os.path.getsize(permanent_path)
            print(f"[DEBUG] Arquivo salvo com sucesso! Tamanho: {final_size} bytes")
        else:
            raise ValueError(f"Falha ao salvar arquivo em: {permanent_path}")
        
        # URL para acessar o arquivo
        audio_url = f"http://localhost:8001/audiofiles/{final_filename}"
        
        # Atualizar registro no banco
        update_data = {
            "status": "completed",
            "audio_url": audio_url,
            "progress": 100,
            "current_step": 5,
            "text_content": text[:1000],  # Salvar primeiros 1000 caracteres
            "file_path": permanent_path,
            "original_file_path": text_file_path  # Referência ao arquivo de texto
        }
        
        audiobooks.update(db, db_obj=db_audiobook, obj_in=update_data)
        
        print(f"[DEBUG] ====== PROCESSAMENTO CONCLUÍDO ======")
        print(f"[DEBUG] URL do áudio: {audio_url}")
        print(f"[DEBUG] Arquivo salvo em: {permanent_path}")
        
        # Limpar apenas arquivos temporários
        try:
            if os.path.exists(temp_narration_path) and temp_narration_path != permanent_path:
                os.remove(temp_narration_path)
            if final_audio_path != narration_path and os.path.exists(final_audio_path) and final_audio_path != permanent_path:
                os.remove(final_audio_path)
        except Exception as e:
            print(f"[AVISO] Erro ao limpar arquivos temporários: {e}")
        
    except Exception as e:
        print(f"[ERRO] Falha no processamento: {str(e)}")
        import traceback
        traceback.print_exc()
        
        audiobooks.update(
            db,
            db_obj=db_audiobook,
            obj_in={
                "status": "error",
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar audiobook: {str(e)}"
        )
    
    return db_audiobook

@router.post("/test-no-auth", response_model=AudiobookResponse)
async def create_audiobook_test(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    """
    Endpoint de teste para criar audiobook sem autenticação.
    Usa um usuário de teste padrão.
    """
    print(f"[DEBUG] Requisição recebida no endpoint de teste")
    print(f"[DEBUG] Nome do arquivo recebido: {file.filename}")
    print(f"[DEBUG] Tipo do arquivo recebido: {file.content_type}")
    
    # Usar usuário de teste
    test_user = User(id=1, email="test@example.com", is_active=True)
    
    # Processar arquivo
    print(f"[DEBUG] Iniciando processamento síncrono")
    
    try:
        # Validar tipo de arquivo
        allowed_types = ['text/plain', 'application/pdf', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")
        
        # Ler conteúdo do arquivo
        file_content = await file.read()
        
        # Extrair texto
        text = extract_text(file_content, file.content_type)
        if not text:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do arquivo")
        
        print(f"[DEBUG] Texto extraído: {text[:100]}...")
        
        # Simular processo assíncrono de forma síncrona
        class DummySelf:
            request = None
        
        # Gerar áudio narração
        narration_path = tempfile.mktemp(suffix=".mp3")
        convert_text_to_speech(DummySelf(), text, narration_path)
        print(f"[DEBUG] Narração gerada: {narration_path}")
        
        # Salvar arquivo diretamente (SEM música de fundo)
        import shutil
        import os
        
        # Criar diretório para áudios se não existir
        audio_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "audiofiles")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        
        # Copiar arquivo final
        audiobook_id = max([0] + [int(f.split('_')[0]) for f in os.listdir() if f.endswith('_audio.mp3')]) + 1
        local_path = f"{audiobook_id}_audio.mp3"
        local_path = os.path.join(audio_dir, local_path)
        shutil.copy2(narration_path, local_path)
        
        audio_url = f"http://localhost:8001/audiofiles/{local_path.split('/')[-1]}"
        
        # Criar registro no banco
        audiobook_data = {
            "title": file.filename,
            "status": "completed",
            "audio_url": audio_url,
            "file_path": local_path,
            "text_content": text[:500],
            "user_id": test_user.id
        }
        audiobook = audiobooks.create(db, obj_in=audiobook_data)
        
        print(f"[DEBUG] Processamento concluído! URL: {audio_url}")
        
        return AudiobookResponse(
            id=audiobook.id,
            title=audiobook.title,
            status=audiobook.status,
            audio_url=audiobook.audio_url,
            created_at=audiobook.created_at
        )
        
    except Exception as e:
        print(f"[DEBUG] Erro no processamento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar audiobook: {str(e)}")

@router.get("/", response_model=List[AudiobookResponse])
def list_audiobooks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Lista todos os audiobooks do usuário.
    """
    return audiobooks.get_multi_by_user(
        db, user_id=1, skip=skip, limit=limit
    )

@router.get("/{audiobook_id}", response_model=AudiobookResponse)
def get_audiobook(
    audiobook_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtém detalhes de um audiobook específico.
    """
    db_audiobook = audiobooks.get(db, id=audiobook_id)
    if not db_audiobook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook não encontrado"
        )
    return db_audiobook

@router.get("/{audiobook_id}/status", response_model=AudiobookStatus)
def get_audiobook_status(
    audiobook_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtém o status atual do processamento do audiobook.
    """
    db_audiobook = audiobooks.get(db, id=audiobook_id)
    if not db_audiobook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook não encontrado"
        )
    return {
        "status": db_audiobook.status,
        "progress": db_audiobook.progress,
        "current_step": db_audiobook.current_step,
        "error": db_audiobook.error
    }

@router.get("/files/list", response_model=dict)
def list_saved_files(
    db: Session = Depends(get_db),
):
    """
    Lista todos os arquivos salvos no sistema (uploads e audiobooks).
    """
    files_info = {
        "uploads": [],
        "audiobooks": [],
        "audiofiles_dir": []
    }
    
    # Listar arquivos de upload
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                files_info["uploads"].append({
                    "filename": filename,
                    "size": os.path.getsize(file_path),
                    "path": file_path,
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
    
    # Listar audiobooks do banco
    audiobooks_list = db.query(audiobooks.model).all()
    for audiobook in audiobooks_list:
        files_info["audiobooks"].append({
            "id": audiobook.id,
            "title": audiobook.title,
            "status": audiobook.status,
            "audio_url": audiobook.audio_url,
            "file_path": audiobook.file_path,
            "original_file_path": audiobook.original_file_path,
            "created_at": audiobook.created_at.isoformat() if audiobook.created_at else None
        })
    
    # Listar arquivos no diretório audiofiles
    if os.path.exists(AUDIO_DIR):
        for filename in os.listdir(AUDIO_DIR):
            file_path = os.path.join(AUDIO_DIR, filename)
            if os.path.isfile(file_path) and filename.endswith('.mp3'):
                files_info["audiofiles_dir"].append({
                    "filename": filename,
                    "size": os.path.getsize(file_path),
                    "path": file_path,
                    "url": f"http://localhost:8001/audiofiles/{filename}",
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
    
    return files_info

@router.delete("/{audiobook_id}/cleanup")
def cleanup_audiobook_files(
    audiobook_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove arquivos de um audiobook específico (apenas para manutenção).
    """
    db_audiobook = audiobooks.get(db, id=audiobook_id)
    if not db_audiobook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook não encontrado"
        )
    
    files_deleted = []
    
    # Remover arquivo de áudio
    if db_audiobook.file_path and os.path.exists(db_audiobook.file_path):
        os.remove(db_audiobook.file_path)
        files_deleted.append(db_audiobook.file_path)
    
    # Remover arquivo original
    if db_audiobook.original_file_path and os.path.exists(db_audiobook.original_file_path):
        os.remove(db_audiobook.original_file_path)
        files_deleted.append(db_audiobook.original_file_path)
    
    # Remover arquivo de texto se existir
    text_file = os.path.join(UPLOAD_DIR, f"{audiobook_id}_texto.txt")
    if os.path.exists(text_file):
        os.remove(text_file)
        files_deleted.append(text_file)
    
    return {
        "message": "Arquivos removidos com sucesso",
        "files_deleted": files_deleted
    }

@router.delete("/{audiobook_id}")
def delete_audiobook(
    audiobook_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove completamente um audiobook (registro do banco + arquivos).
    """
    db_audiobook = audiobooks.get(db, id=audiobook_id)
    if not db_audiobook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook não encontrado"
        )
    
    files_deleted = []
    
    # Remover arquivo de áudio principal
    if db_audiobook.file_path and os.path.exists(db_audiobook.file_path):
        try:
            os.remove(db_audiobook.file_path)
            files_deleted.append(db_audiobook.file_path)
        except Exception as e:
            print(f"[WARN] Erro ao remover arquivo de áudio: {e}")
    
    # Remover arquivo original
    if db_audiobook.original_file_path and os.path.exists(db_audiobook.original_file_path):
        try:
            os.remove(db_audiobook.original_file_path)
            files_deleted.append(db_audiobook.original_file_path)
        except Exception as e:
            print(f"[WARN] Erro ao remover arquivo original: {e}")
    
    # Remover arquivo de texto se existir
    text_file = os.path.join(UPLOAD_DIR, f"{audiobook_id}_texto.txt")
    if os.path.exists(text_file):
        try:
            os.remove(text_file)
            files_deleted.append(text_file)
        except Exception as e:
            print(f"[WARN] Erro ao remover arquivo de texto: {e}")
    
    # Tentar remover arquivo do diretório audiofiles com padrão do ID
    try:
        import glob
        audiofiles_pattern = os.path.join(AUDIO_DIR, f"{audiobook_id}_*.mp3")
        audiofiles_matches = glob.glob(audiofiles_pattern)
        for audio_file in audiofiles_matches:
            if os.path.exists(audio_file):
                os.remove(audio_file)
                files_deleted.append(audio_file)
    except Exception as e:
        print(f"[WARN] Erro ao remover arquivos de áudio: {e}")
    
    # Remover registro do banco de dados
    audiobooks.remove(db, id=audiobook_id)
    
    return {
        "message": f"Audiobook {audiobook_id} removido com sucesso",
        "files_deleted": files_deleted,
        "audiobook_title": db_audiobook.title
    }
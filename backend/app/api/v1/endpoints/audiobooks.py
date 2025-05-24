from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.schemas.audiobook import AudiobookCreate, AudiobookResponse, AudiobookStatus
from app.crud import audiobooks
from app.tasks.audiobook import process_audiobook
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=AudiobookResponse)
async def create_audiobook(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo audiobook a partir de um arquivo de texto.
    """
    # Validar tipo do arquivo
    if not file.content_type in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de arquivo não suportado"
        )
    
    # Criar registro do audiobook
    audiobook_data = AudiobookCreate(
        title=file.filename,
        status="processing",
        user_id=current_user.id
    )
    db_audiobook = audiobooks.create(db, obj_in=audiobook_data)
    
    # Iniciar processamento assíncrono
    process_audiobook.delay(
        audiobook_id=db_audiobook.id,
        file_content=file.file.read(),
        file_type=file.content_type
    )
    
    return db_audiobook

@router.get("/", response_model=List[AudiobookResponse])
def list_audiobooks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os audiobooks do usuário.
    """
    return audiobooks.get_multi_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )

@router.get("/{audiobook_id}", response_model=AudiobookResponse)
def get_audiobook(
    audiobook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém detalhes de um audiobook específico.
    """
    db_audiobook = audiobooks.get(db, id=audiobook_id)
    if not db_audiobook or db_audiobook.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook não encontrado"
        )
    return db_audiobook

@router.get("/{audiobook_id}/status", response_model=AudiobookStatus)
def get_audiobook_status(
    audiobook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém o status atual do processamento do audiobook.
    """
    db_audiobook = audiobooks.get(db, id=audiobook_id)
    if not db_audiobook or db_audiobook.user_id != current_user.id:
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
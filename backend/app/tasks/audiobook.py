import io
import tempfile
from celery import Task
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.crud import audiobooks
from PyPDF2 import PdfReader
from docx import Document
from gtts import gTTS
import boto3
import os

class AudiobookTask(Task):
    _db = None
    _s3 = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    @property
    def s3(self):
        if self._s3 is None:
            self._s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        return self._s3

@celery_app.task(bind=True, base=AudiobookTask)
def process_audiobook(self, audiobook_id: int, file_content: bytes, file_type: str):
    """
    Processa o arquivo de texto e gera o audiobook.
    """
    try:
        # Atualizar status
        audiobook = audiobooks.get(self.db, id=audiobook_id)
        audiobook.current_step = 0
        audiobook.progress = 0
        self.db.commit()

        # Extrair texto do arquivo
        text = extract_text(file_content, file_type)
        audiobook.current_step = 1
        audiobook.progress = 20
        self.db.commit()

        # Identificar personagens (simulado)
        characters = identify_characters(text)
        audiobook.current_step = 2
        audiobook.progress = 40
        self.db.commit()

        # Gerar áudio
        audio_path = generate_audio(text, characters)
        audiobook.current_step = 3
        audiobook.progress = 60
        self.db.commit()

        # Adicionar trilha sonora (simulado)
        final_audio_path = add_background_music(audio_path)
        audiobook.current_step = 4
        audiobook.progress = 80
        self.db.commit()

        # Upload para S3
        s3_url = upload_to_s3(self.s3, final_audio_path, audiobook_id)
        
        # Atualizar audiobook
        audiobooks.update(
            self.db,
            db_obj=audiobook,
            obj_in={
                "status": "completed",
                "audio_url": s3_url,
                "progress": 100,
                "current_step": 5
            }
        )
        self.db.commit()

        # Limpar arquivos temporários
        os.remove(audio_path)
        os.remove(final_audio_path)

    except Exception as e:
        audiobooks.update(
            self.db,
            db_obj=audiobook,
            obj_in={
                "status": "error",
                "error": str(e)
            }
        )
        self.db.commit()
        raise

def extract_text(file_content: bytes, file_type: str) -> str:
    """
    Extrai texto do arquivo baseado no tipo.
    """
    content = io.BytesIO(file_content)
    
    if file_type == "application/pdf":
        reader = PdfReader(content)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(content)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    else:  # text/plain
        text = content.read().decode()
    
    return text

def identify_characters(text: str) -> dict:
    """
    Identifica personagens no texto (versão simulada).
    """
    return {
        "narrator": "natural",
        "character1": "masculina",
        "character2": "feminina"
    }

def generate_audio(text: str, characters: dict) -> str:
    """
    Gera áudio a partir do texto usando Amazon Polly.
    """
    polly = boto3.client(
        'polly',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Camila",  # Voz feminina brasileira
        LanguageCode="pt-BR"
    )
    temp_path = tempfile.mktemp(suffix='.mp3')
    with open(temp_path, "wb") as file:
        file.write(response['AudioStream'].read())
    return temp_path

def add_background_music(audio_path: str) -> str:
    """
    Adiciona trilha sonora ao áudio (versão simulada).
    """
    # Aqui você pode adicionar lógica real de processamento de áudio
    return audio_path

def upload_to_s3(s3_client, file_path: str, audiobook_id: int) -> str:
    """
    Faz upload do arquivo para o S3.
    """
    key = f"audiobooks/{audiobook_id}/audio.mp3"
    s3_client.upload_file(
        file_path,
        settings.AWS_BUCKET_NAME,
        key
    )
    return f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{key}" 
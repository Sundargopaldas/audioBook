import io
import tempfile
from celery import Task
from app.core.celery_app import celery_app  # Alterado
from app.core.config import settings      # Alterado
from app.db.session import SessionLocal     # Alterado
from app.crud import audiobooks             # Alterado
from PyPDF2 import PdfReader
from docx import Document
import boto3
import os
from google.cloud import texttospeech
from pydub import AudioSegment
import random
import re

# Adicionar FFmpeg ao PATH se estiver no Windows
import sys
if sys.platform == "win32":
    ffmpeg_path = r"C:\ffmpeg\bin"
    if os.path.exists(ffmpeg_path) and ffmpeg_path not in os.environ['PATH']:
        os.environ['PATH'] = os.environ['PATH'] + ';' + ffmpeg_path

# Configurar variável de ambiente para Google Cloud TTS
# Usando caminho absoluto para garantir que funcione
google_creds_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', settings.GOOGLE_APPLICATION_CREDENTIALS)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(google_creds_path)

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
        # Debug: Save extracted text to a temporary file
        text_file_path = tempfile.mktemp(suffix='.txt')
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Debug: Extracted text saved to {text_file_path}")

        audiobook.current_step = 1
        audiobook.progress = 20
        self.db.commit()

        # Identificar personagens (simulado)
        characters = identify_characters(text)
        audiobook.current_step = 2
        audiobook.progress = 40
        self.db.commit()

        # Gerar áudio da narração
        narration_audio_path = convert_text_to_speech(self, text, tempfile.mktemp(suffix='.mp3'))
        # Debug: Save narration audio to a temporary file
        print(f"Debug: Narration audio saved to {narration_audio_path}")

        audiobook.current_step = 3
        audiobook.progress = 60
        self.db.commit()

        # Adicionar trilha sonora (simulado) e combinar com narração
        final_audio_path = add_background_music(narration_audio_path)
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
        os.remove(narration_audio_path)
        os.remove(final_audio_path)
        os.remove(text_file_path) # Clean up debug file

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

def add_background_music(narration_audio_path: str) -> str:
    """
    Adiciona trilha sonora ao áudio da narração.
    
    Args:
        narration_audio_path: Caminho do arquivo de narração
        
    Returns:
        Caminho do arquivo de áudio final com música de fundo
    """
    try:
        # Carregar o áudio da narração
        narration = AudioSegment.from_mp3(narration_audio_path)
        
        # Verificar se existem músicas de fundo disponíveis
        music_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'background_music')
        music_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3') and f != 'README.md']
        
        if not music_files:
            print("Nenhuma música de fundo encontrada. Retornando apenas a narração.")
            return narration_audio_path
        
        # Selecionar uma música aleatória
        music_file = random.choice(music_files)
        music_path = os.path.join(music_dir, music_file)
        print(f"Usando música de fundo: {music_file}")
        
        # Carregar a música de fundo
        background_music = AudioSegment.from_mp3(music_path)
        
        # Ajustar o volume da música de fundo (reduzir para -15dB para ficar mais audível)
        background_music = background_music - 15
        
        # Fazer loop da música se ela for menor que a narração
        narration_length = len(narration)
        music_length = len(background_music)
        
        if music_length < narration_length:
            # Repetir a música até cobrir toda a narração
            times_to_repeat = (narration_length // music_length) + 1
            background_music = background_music * times_to_repeat
        
        # Cortar a música para ter o mesmo tamanho da narração
        background_music = background_music[:narration_length]
        
        # Fazer fade in e fade out na música (3 segundos)
        background_music = background_music.fade_in(3000).fade_out(3000)
        
        # Mixar narração com música de fundo
        final_audio = narration.overlay(background_music)
        
        # Salvar o áudio final
        output_path = narration_audio_path.replace('.mp3', '_with_music.mp3')
        final_audio.export(output_path, format="mp3")
        
        print(f"Áudio com música de fundo salvo em: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Erro ao adicionar música de fundo: {str(e)}")
        print("Retornando apenas a narração.")
        return narration_audio_path

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

def convert_text_to_speech(self, text: str, output_file: str) -> str:
    """
    Converte texto em áudio usando Google Cloud Text-to-Speech com voz de alta qualidade.
    Para textos grandes, quebra em chunks e combina os áudios.
    
    Args:
        text: Texto a ser convertido
        output_file: Caminho do arquivo de saída
    
    Returns:
        Caminho do arquivo de áudio gerado
    """
    try:
        # Pré-processar o texto para melhorar a pronúncia
        processed_text = preprocess_text_for_tts(text)
        
        # Verificar se o texto está dentro do limite do Google Cloud TTS (5000 bytes)
        text_bytes = processed_text.encode('utf-8')
        
        if len(text_bytes) <= 4800:  # Margem de segurança
            # Texto pequeno - usar diretamente o Google Cloud TTS
            return generate_single_audio_segment(processed_text, output_file)
        else:
            # Texto grande - quebrar em chunks e combinar
            print(f"[INFO] Texto grande ({len(text_bytes)} bytes). Quebrando em segmentos...")
            return generate_audio_from_chunks(processed_text, output_file)
            
    except Exception as e:
        print(f"Erro geral na geração de áudio: {str(e)}")
        # Fallback final para gTTS como último recurso
        print("Usando fallback gTTS...")
        return fallback_to_gtts(text, output_file)

def create_custom_phonetic_dict(additional_names: dict = None) -> dict:
    """
    Cria um dicionário de substituições fonéticas personalizadas.
    
    Args:
        additional_names: Dicionário adicional de nomes para substituições
        
    Returns:
        Dicionário completo de substituições fonéticas
    """
    # Dicionário base
    base_replacements = {
        # Nomes de lugares e personagens principais
        'Kanzime': 'Canzimi',
        'Timuth': 'Timute',
        'Hefra': 'Éfra', 
        'Ranthari': 'Rantári',
        'Tardia': 'Tárdia',
        'Eknon': 'Écnon',
        'Arthianto': 'Artianto',
        'Arighon': 'Arigon',
        'Belfs': 'Belefes',
        'Markus': 'Márcus',
        'Lyra': 'Líra',
        'Theo': 'Téo',
        'Viktor': 'Víctor',
        'Aldric': 'Áldric',
        'Edmund': 'Edmundo',
        
        # Termos de fantasia comuns
        'mana': 'mána',
        'mage': 'mago',
        'guild': 'guilda',
        'quest': 'missão',
        'dungeon': 'masmorra',
        'boss': 'chefe',
        'raid': 'incursão',
        
        # RPG e Gaming
        'HP': 'pontos de vida',
        'MP': 'pontos de mana',
        'EXP': 'experiência',
        'XP': 'experiência',
        'LVL': 'nível',
        'STR': 'força',
        'DEX': 'destreza',
        'INT': 'inteligência',
        'WIS': 'sabedoria',
        'CON': 'constituição',
        'CHA': 'carisma',
        'AGI': 'agilidade',
        'VIT': 'vitalidade',
        
        # Termos técnicos
        'AI': 'inteligência artificial',
        'NPC': 'personagem não jogável',
        'PvP': 'jogador contra jogador',
        'PvE': 'jogador contra ambiente',
        'DPS': 'dano por segundo',
        'AOE': 'área de efeito',
        'DOT': 'dano contínuo',
        'HOT': 'cura contínua',
        'CC': 'controle de grupo',
        'CD': 'tempo de recarga',
        
        # Nomes fantásticos comuns que podem ser soletrados
        'Eldar': 'Éldar',
        'Dwarven': 'Anão',
        'Elvish': 'Élfico',
        'Orcish': 'Órquico',
        'Draconic': 'Dracônico',
        'Celestial': 'Celestial',
        'Infernal': 'Infernal',
        'Sylvan': 'Silvestre',
        'Primordial': 'Primordial',
        
        # Melhorar pronúncia de alguns termos em inglês comuns
        'the': 'o',
        'and': 'e',
        'of': 'de',
        'to': 'para',
        'in': 'em',
        'is': 'é',
        'that': 'que',
        'for': 'para',
        'with': 'com',
        'as': 'como',
    }
    
    # Adicionar nomes personalizados se fornecidos
    if additional_names:
        base_replacements.update(additional_names)
    
    return base_replacements

def preprocess_text_for_tts(text: str, custom_names: dict = None) -> str:
    """
    Pré-processa o texto para melhorar a qualidade da síntese de voz.
    Inclui tratamento especial para nomes próprios e palavras que podem ser soletradas.
    
    Args:
        text: Texto a ser processado
        custom_names: Dicionário adicional de substituições personalizadas
    """
    # Obter dicionário de substituições fonéticas
    phonetic_replacements = create_custom_phonetic_dict(custom_names)
    
    # Aplicar substituições fonéticas (case-insensitive)
    for original, replacement in phonetic_replacements.items():
        # Substituir mantendo a capitalização original
        pattern = re.escape(original)
        
        def replace_func(match):
            matched_word = match.group(0)
            if matched_word.isupper():
                return replacement.upper()
            elif matched_word.istitle():
                return replacement.capitalize()
            else:
                return replacement.lower()
        
        # Usar word boundaries para evitar substituições parciais
        text = re.sub(r'\b' + pattern + r'\b', replace_func, text, flags=re.IGNORECASE)
    
    # Tratamento especial para nomes compostos com hífen ou apóstrofo
    text = re.sub(r"([A-Za-z]+)['-]([A-Za-z]+)", r'\1 \2', text)
    
    # Melhorar pronúncia de números e ordinais
    text = re.sub(r'\b(\d+)º\b', r'\1° ', text)  # Ordinais
    text = re.sub(r'\b(\d+)ª\b', r'\1ª ', text)  # Ordinais femininos
    text = re.sub(r'\b(\d+)\s*[xX]\s*(\d+)\b', r'\1 por \2', text)  # Dimensões
    
    # Melhorar pontuação para pausas mais naturais
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Normalizar quebras de linha
    text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)  # Pausas após pontuação
    
    # Tratamento especial para títulos de capítulos
    text = re.sub(r'(CAPÍTULO\s+\d+[^\n]*)\n', r'\1.\n\n', text)
    text = re.sub(r'(PARTE\s+\d+[^\n]*)\n', r'\1.\n\n', text)
    text = re.sub(r'(SEÇÃO\s+\d+[^\n]*)\n', r'\1.\n\n', text)
    
    # Melhorar pronúncia de diálogos
    text = re.sub(r'["""]([^"""]*)["""]', r'"\1"', text)  # Normalizar aspas
    
    # Tratar onomatopeias comuns
    onomatopeias = {
        'hahaha': 'rá rá rá',
        'hehehe': 'ré ré ré', 
        'kkkk': 'ká ká ká',
        'rsrsrs': 'érre érre érre',
        'hmmm': 'hum',
        'uhum': 'áhã',
        'zzz': 'zzz dormindo',
    }
    
    for ono, replacement in onomatopeias.items():
        text = re.sub(r'\b' + re.escape(ono) + r'\b', replacement, text, flags=re.IGNORECASE)
    
    # Adicionar pausas sutis em listas e enumerações
    text = re.sub(r'([,;])\s*', r'\1 ', text)
    text = re.sub(r':\s*', r': ', text)
    
    # Normalizar espaços
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def generate_single_audio_segment(text: str, output_file: str) -> str:
    """
    Gera áudio para um único segmento de texto usando Google Cloud TTS.
    """
    try:
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            name="pt-BR-Chirp3-HD-Achernar"
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,  # Velocidade normal
            pitch=0.0,          # Tom normal
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            
        print(f"Áudio gerado com sucesso usando Google Cloud TTS: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Erro ao gerar áudio com Google Cloud TTS: {str(e)}")
        raise

def generate_audio_from_chunks(text: str, output_file: str) -> str:
    """
    Quebra texto grande em chunks e combina os áudios gerados.
    """
    try:
        # Quebrar texto em chunks inteligentes
        chunks = split_text_intelligently(text, max_bytes=4500)
        print(f"[INFO] Texto dividido em {len(chunks)} segmentos")
        
        # Gerar áudio para cada chunk
        audio_segments = []
        temp_files = []
        
        for i, chunk in enumerate(chunks):
            print(f"[INFO] Processando segmento {i+1}/{len(chunks)}")
            
            temp_file = tempfile.mktemp(suffix=f'_chunk_{i}.mp3')
            temp_files.append(temp_file)
            
            try:
                generate_single_audio_segment(chunk, temp_file)
                audio_segment = AudioSegment.from_mp3(temp_file)
                
                # Adicionar pequena pausa entre segmentos (500ms)
                if i > 0:
                    pause = AudioSegment.silent(duration=500)
                    audio_segments.append(pause)
                
                audio_segments.append(audio_segment)
                
            except Exception as e:
                print(f"[ERRO] Falha no segmento {i+1}: {str(e)}")
                # Tentar com gTTS para este segmento específico
                chunk_gtts_file = tempfile.mktemp(suffix=f'_gtts_chunk_{i}.mp3')
                temp_files.append(chunk_gtts_file)
                fallback_to_gtts(chunk, chunk_gtts_file)
                audio_segment = AudioSegment.from_mp3(chunk_gtts_file)
                
                if i > 0:
                    pause = AudioSegment.silent(duration=500)
                    audio_segments.append(pause)
                
                audio_segments.append(audio_segment)
        
        # Combinar todos os segmentos
        if audio_segments:
            combined_audio = audio_segments[0]
            for segment in audio_segments[1:]:
                combined_audio += segment
            
            # Salvar áudio combinado
            combined_audio.export(output_file, format="mp3")
            print(f"[INFO] Áudio combinado salvo em: {output_file}")
        
        # Limpar arquivos temporários
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        
        return output_file
        
    except Exception as e:
        print(f"Erro ao gerar áudio de chunks: {str(e)}")
        raise

def split_text_intelligently(text: str, max_bytes: int = 4500) -> list:
    """
    Quebra o texto em chunks inteligentes respeitando parágrafos e frases.
    """
    chunks = []
    
    # Primeiro, tentar quebrar por parágrafos
    paragraphs = text.split('\n\n')
    current_chunk = ""
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Verificar se adicionar este parágrafo ultrapassa o limite
        test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
        
        if len(test_chunk.encode('utf-8')) <= max_bytes:
            current_chunk = test_chunk
        else:
            # Se o chunk atual não está vazio, salvá-lo
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            # Se o parágrafo sozinho é muito grande, quebrar por frases
            if len(paragraph.encode('utf-8')) > max_bytes:
                sentence_chunks = split_paragraph_by_sentences(paragraph, max_bytes)
                chunks.extend(sentence_chunks)
            else:
                current_chunk = paragraph
    
    # Adicionar o último chunk se houver
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def split_paragraph_by_sentences(paragraph: str, max_bytes: int) -> list:
    """
    Quebra um parágrafo por frases quando ele é muito grande.
    """
    chunks = []
    
    # Quebrar por frases (pontos, exclamações, interrogações)
    sentences = re.split(r'([.!?]+\s*)', paragraph)
    current_chunk = ""
    
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        
        # Se é uma pontuação, juntar com a frase anterior
        if i + 1 < len(sentences) and re.match(r'[.!?]+\s*', sentences[i + 1]):
            sentence += sentences[i + 1]
            i += 2
        else:
            i += 1
        
        test_chunk = current_chunk + sentence if current_chunk else sentence
        
        if len(test_chunk.encode('utf-8')) <= max_bytes:
            current_chunk = test_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # Se uma única frase é muito grande, forçar quebra por caracteres
                chunks.append(sentence[:max_bytes//2])
                current_chunk = sentence[max_bytes//2:]
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def fallback_to_gtts(text: str, output_file: str) -> str:
    """
    Fallback para gTTS com melhor configuração.
    """
    try:
        from gtts import gTTS
        
        # Pré-processar texto para gTTS também
        processed_text = preprocess_text_for_tts(text)
        
        # Usar gTTS com configurações otimizadas
        tts = gTTS(
            text=processed_text, 
            lang='pt',  # Português genérico para melhor compatibilidade
            slow=False  # Velocidade normal
        )
        tts.save(output_file)
        
        print(f"Áudio gerado usando gTTS: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Erro no fallback gTTS: {str(e)}")
        raise
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

# Configurar a variável de ambiente
google_creds_path = os.path.join(os.path.dirname(__file__), '..', settings.GOOGLE_APPLICATION_CREDENTIALS)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(google_creds_path)

print(f"GOOGLE_APPLICATION_CREDENTIALS configurado para: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
print(f"Arquivo existe: {os.path.exists(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])}")

try:
    from google.cloud import texttospeech
    
    # Testar a conexão
    client = texttospeech.TextToSpeechClient()
    
    # Testar uma síntese simples
    synthesis_input = texttospeech.SynthesisInput(text="Teste de configuração do Google Cloud TTS")
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Chirp3-HD-Achernar"
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Salvar o teste
    with open("test_backend_tts.mp3", "wb") as out:
        out.write(response.audio_content)
        print("✅ Teste bem-sucedido! Áudio salvo como test_backend_tts.mp3")
        
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    print("\nVerifique se:")
    print("1. O arquivo google-tts-key.json existe no diretório raiz do projeto")
    print("2. As credenciais no arquivo são válidas")
    print("3. A biblioteca google-cloud-texttospeech está instalada") 
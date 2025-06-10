from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(text="Olá, este é um teste de voz natural do Google Cloud!")

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

with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Áudio salvo como output.mp3") 
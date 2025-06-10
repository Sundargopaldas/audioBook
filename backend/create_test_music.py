from pydub import AudioSegment
from pydub.generators import Sine
import os

print("Criando música de teste...")

# Criar um tom simples para teste (440Hz - nota Lá)
tone = Sine(440).to_audio_segment(duration=30000)  # 30 segundos

# Reduzir o volume
tone = tone - 30  # Reduzir 30dB

# Adicionar fade in e fade out
tone = tone.fade_in(2000).fade_out(2000)

# Salvar como MP3
output_path = os.path.join("background_music", "música_teste.mp3")
tone.export(output_path, format="mp3")

print(f"Música de teste criada em: {output_path}")
print("NOTA: Esta é apenas uma música de teste. Para produção, adicione músicas reais na pasta background_music/") 
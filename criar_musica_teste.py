import os
import sys
sys.path.append('backend')

from pydub import AudioSegment
from pydub.generators import Sine

print("Criando música de fundo de teste...")

# Criar uma melodia simples e relaxante
duration_ms = 60000  # 60 segundos

# Criar tons suaves
frequencies = [261.63, 329.63, 392.00, 440.00]  # C, E, G, A

# Criar a música completa
full_music = AudioSegment.silent(duration=0)

# Criar padrão repetitivo
for _ in range(15):  # Repetir 15 vezes
    for freq in frequencies:
        # Criar tom de 1 segundo
        tone = Sine(freq).to_audio_segment(duration=1000)
        
        # Reduzir volume
        tone = tone - 25
        
        # Adicionar fade in/out
        tone = tone.fade_in(100).fade_out(100)
        
        # Adicionar ao áudio completo
        full_music += tone

# Aplicar fade in/out geral
full_music = full_music.fade_in(3000).fade_out(3000)

# Salvar
output_dir = os.path.join("backend", "background_music")
output_path = os.path.join(output_dir, "música_calma.mp3")

# Criar diretório se não existir
os.makedirs(output_dir, exist_ok=True)

# Exportar como MP3
full_music.export(output_path, format="mp3", bitrate="192k")

print(f"\n✓ Música de fundo criada com sucesso!")
print(f"  Arquivo: {output_path}")
print(f"  Duração: 60 segundos")
print(f"  Tipo: Melodia calma e relaxante")
print("\nAgora o sistema irá adicionar automaticamente esta música de fundo aos audiobooks!")
print("\nPara adicionar suas próprias músicas:")
print(f"1. Coloque arquivos MP3 em: {output_dir}")
print("2. O sistema selecionará uma música aleatoriamente")
print("3. Volume e fade in/out são aplicados automaticamente") 
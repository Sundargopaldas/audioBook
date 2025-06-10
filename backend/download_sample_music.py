import os
import urllib.request

# URL de uma música gratuita do Free Music Archive
# Esta é uma música calma, instrumental, perfeita para fundo
music_url = "https://freepd.com/music/Chill%20Wave.mp3"
output_path = os.path.join("background_music", "música_calma.mp3")

print("Baixando música de fundo gratuita para teste...")
try:
    urllib.request.urlretrieve(music_url, output_path)
    print(f"Música baixada com sucesso em: {output_path}")
except Exception as e:
    print(f"Erro ao baixar música: {e}")
    print("Por favor, adicione manualmente arquivos MP3 na pasta background_music/") 
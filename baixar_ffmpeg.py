import os
import urllib.request
import zipfile
import shutil

print("=== INSTALADOR DO FFMPEG PARA WINDOWS ===\n")

# URL do FFmpeg para Windows
ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
download_path = "ffmpeg.zip"
extract_path = "ffmpeg_temp"
final_path = "C:\\ffmpeg"

print("1. Baixando FFmpeg...")
try:
    urllib.request.urlretrieve(ffmpeg_url, download_path)
    print("   ✓ Download concluído!")
except Exception as e:
    print(f"   ✗ Erro ao baixar: {e}")
    print("\nAlternativa: Baixe manualmente de https://www.gyan.dev/ffmpeg/builds/")
    exit(1)

print("\n2. Extraindo arquivos...")
try:
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("   ✓ Extração concluída!")
except Exception as e:
    print(f"   ✗ Erro ao extrair: {e}")
    exit(1)

print("\n3. Movendo para C:\\ffmpeg...")
try:
    # Encontrar a pasta extraída
    extracted_folder = None
    for item in os.listdir(extract_path):
        if item.startswith("ffmpeg") and os.path.isdir(os.path.join(extract_path, item)):
            extracted_folder = item
            break
    
    if extracted_folder:
        source = os.path.join(extract_path, extracted_folder)
        
        # Remover pasta anterior se existir
        if os.path.exists(final_path):
            shutil.rmtree(final_path)
        
        # Mover para C:\ffmpeg
        shutil.move(source, final_path)
        print("   ✓ FFmpeg instalado em C:\\ffmpeg")
    else:
        print("   ✗ Pasta do ffmpeg não encontrada")
        exit(1)
except Exception as e:
    print(f"   ✗ Erro ao mover arquivos: {e}")
    exit(1)

print("\n4. Limpando arquivos temporários...")
try:
    os.remove(download_path)
    shutil.rmtree(extract_path)
    print("   ✓ Limpeza concluída!")
except:
    pass

print("\n=== INSTALAÇÃO CONCLUÍDA! ===")
print("\nPRÓXIMOS PASSOS:")
print("1. Adicione C:\\ffmpeg\\bin ao PATH do Windows:")
print("   - Abra 'Variáveis de Ambiente' no Painel de Controle")
print("   - Em 'Variáveis do Sistema', encontre 'Path'")
print("   - Clique em 'Editar' e adicione: C:\\ffmpeg\\bin")
print("   - Clique OK e reinicie o PowerShell")
print("\n2. Teste executando: ffmpeg -version")
print("\n3. Adicione músicas MP3 em: backend\\background_music\\")
print("\nO sistema já está preparado para usar música de fundo!") 
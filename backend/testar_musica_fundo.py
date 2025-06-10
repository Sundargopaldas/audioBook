"""
Script para testar a música de fundo dos audiobooks
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pydub import AudioSegment
from pydub.playback import play

def verificar_musica_fundo():
    """Verifica se os audiobooks têm música de fundo"""
    
    audiofiles_dir = os.path.join(os.path.dirname(__file__), "audiofiles")
    
    print("🎵 VERIFICANDO MÚSICA DE FUNDO NOS AUDIOBOOKS")
    print("=" * 50)
    
    # Listar todos os audiobooks
    audiobooks = [f for f in os.listdir(audiofiles_dir) if f.endswith("_audiobook_completo.mp3")]
    
    if not audiobooks:
        print("❌ Nenhum audiobook encontrado!")
        return
    
    print(f"\n📚 {len(audiobooks)} audiobooks encontrados:")
    
    for audiobook in audiobooks:
        filepath = os.path.join(audiofiles_dir, audiobook)
        
        # Carregar o áudio
        audio = AudioSegment.from_mp3(filepath)
        
        # Analisar o áudio
        print(f"\n🎧 {audiobook}")
        print(f"   • Duração: {len(audio) / 1000:.1f} segundos")
        print(f"   • Volume RMS: {audio.rms}")
        print(f"   • Volume máximo: {audio.max}")
        
        # Extrair um trecho do meio (onde a música deve estar mais clara)
        meio = len(audio) // 2
        trecho = audio[meio:meio + 5000]  # 5 segundos do meio
        
        # Verificar se há variação no volume (indicativo de música + voz)
        if trecho.rms > audio.rms * 0.8:
            print(f"   ✅ Provável música de fundo detectada!")
        else:
            print(f"   ⚠️ Música de fundo pode estar muito baixa")
    
    print("\n💡 DICA: Para ouvir melhor a música de fundo:")
    print("   1. Use fones de ouvido")
    print("   2. Aumente o volume")
    print("   3. Preste atenção no fundo durante as pausas da narração")

if __name__ == "__main__":
    verificar_musica_fundo() 
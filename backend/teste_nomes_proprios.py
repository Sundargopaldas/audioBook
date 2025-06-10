import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tasks.audiobook import convert_text_to_speech, preprocess_text_for_tts

# Texto de teste focado nos nomes próprios que eram soletrados
texto_nomes = """
TESTE DE PRONÚNCIA DE NOMES PRÓPRIOS

Os heróis de Kanzime se reuniram no reino de Arthianto. Timuth, Hefra, Ranthari e Tardia chegaram à cidade de Eknon para enfrentar os terríveis Belfs.

Markus, o grande general, encontrou-se com a sacerdotisa Lyra no penhasco de Arighon. O inventor Theo mostrou suas criações para Viktor, enquanto o comerciante Aldric negociava com o jovem nobre Edmund.

"Kanzime precisa de nossos heróis!" gritou Timuth. 
"Os Belfs atacaram Arthianto!" respondeu Hefra.
"Devemos proteger Eknon!" declarou Ranthari.
"Unidos por Kanzime!" concluiu Tardia.

O destino de Kanzime estava nas mãos dos valorosos guerreiros de Arthianto.
""".strip()

print("=== TESTE DE NOMES PRÓPRIOS ===")
print(f"Texto original:")
print(texto_nomes[:200] + "...")
print(f"\nTamanho: {len(texto_nomes)} caracteres")

# Testar pré-processamento
print("\n--- Testando pré-processamento ---")
texto_processado = preprocess_text_for_tts(texto_nomes)
print("Texto após pré-processamento:")
print(texto_processado[:200] + "...")

# Mostrar diferenças específicas
print("\n--- Substituições aplicadas ---")
original_names = ['Kanzime', 'Timuth', 'Hefra', 'Ranthari', 'Tardia', 'Arthianto', 'Eknon', 'Belfs', 'Markus', 'Lyra', 'Arighon', 'Theo', 'Viktor', 'Aldric', 'Edmund']

for name in original_names:
    if name in texto_nomes and name.lower() not in texto_processado.lower():
        print(f"✅ {name} foi substituído")
    elif name in texto_nomes:
        # Procurar pela versão modificada
        if name == 'Kanzime' and 'canzimi' in texto_processado.lower():
            print(f"✅ {name} → Canzimi")
        elif name == 'Timuth' and 'timute' in texto_processado.lower():
            print(f"✅ {name} → Timute")
        elif name == 'Hefra' and 'éfra' in texto_processado.lower():
            print(f"✅ {name} → Éfra")
        else:
            print(f"⚠️ {name} ainda presente")

# Testar TTS melhorado
print("\n--- Testando TTS com nomes melhorados ---")
class DummySelf:
    pass

output_file = "teste_nomes_proprios_melhorado.mp3"
try:
    print("Iniciando geração de áudio...")
    result = convert_text_to_speech(DummySelf(), texto_nomes, output_file)
    print(f"✅ Áudio gerado com sucesso: {result}")
    
    if os.path.exists(result):
        size = os.path.getsize(result)
        print(f"Tamanho do arquivo gerado: {size} bytes")
        print(f"Duração estimada: ~{size/32000:.1f} segundos")
    else:
        print("❌ Arquivo não foi criado")
        
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE CONCLUÍDO ===")
print("🎧 Por favor, escute o arquivo gerado para verificar se:")
print("1. 'Kanzime' é pronunciado como 'Canzimi' (não soletrado)")
print("2. Outros nomes próprios têm pronúncia melhorada")
print("3. A qualidade geral da narração está boa") 
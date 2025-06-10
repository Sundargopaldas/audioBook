"""
Utilitário para adicionar nomes personalizados ao dicionário fonético.
Use este arquivo para testar novos nomes e suas pronúncias antes de adicioná-los ao sistema principal.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tasks.audiobook import convert_text_to_speech, preprocess_text_for_tts

def testar_pronucia_personalizada():
    """
    Teste interativo para adicionar e testar novos nomes próprios.
    """
    print("=== TESTE DE PRONÚNCIA PERSONALIZADA ===\n")
    
    # Nomes personalizados adicionais - ADICIONE AQUI SEUS NOMES
    nomes_personalizados = {
        # Exemplo: 'Nome_Original': 'Pronuncia_Melhorada',
        'Xerath': 'Xérat',
        'Zythara': 'Zitára', 
        'Korvain': 'Corvain',
        'Sylthris': 'Siltris',
        'Drakmoor': 'Dracmor',
        'Vex': 'Vécs',
        'Nyx': 'Nics',
        'Zul': 'Zul',
        
        # Adicione mais nomes aqui conforme necessário
        # 'SeuNome': 'ComoDevePronunciar',
    }
    
    # Texto de teste com os nomes personalizados
    texto_teste = f"""
    TESTE DE NOMES PERSONALIZADOS
    
    Os guerreiros Xerath e Zythara partiram de Korvain rumo à cidade de Sylthris. 
    
    Em Drakmoor, o mago Vex encontrou a assassina Nyx, que havia sido enviada por Zul.
    
    "Xerath protegerá Zythara!" declarou Korvain.
    "Sylthris aguarda por Drakmoor!" respondeu Vex.
    "Nyx e Zul não prevalecerão!" concluiu a batalha.
    
    E assim, os heróis de Xerath, Zythara, Korvain e Sylthris derrotaram as forças de Drakmoor, Vex, Nyx e Zul.
    """
    
    print("Texto original:")
    print(texto_teste)
    print("\n" + "="*50 + "\n")
    
    # Aplicar pré-processamento com nomes personalizados
    texto_processado = preprocess_text_for_tts(texto_teste.strip(), nomes_personalizados)
    
    print("Texto após substituições fonéticas:")
    print(texto_processado)
    print("\n" + "="*50 + "\n")
    
    # Mostrar substituições realizadas
    print("Substituições aplicadas:")
    for original, melhorado in nomes_personalizados.items():
        if original.lower() in texto_teste.lower():
            if original.lower() not in texto_processado.lower():
                print(f"✅ {original} → {melhorado}")
            else:
                print(f"⚠️ {original} não foi substituído (verifique se está correto)")
    
    print("\n" + "="*50 + "\n")
    
    # Gerar áudio de teste
    resposta = input("Deseja gerar áudio de teste? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\nGerando áudio de teste...")
        
        class DummySelf:
            pass
        
        output_file = "teste_nomes_personalizados.mp3"
        
        try:
            result = convert_text_to_speech(DummySelf(), texto_teste.strip(), output_file)
            print(f"✅ Áudio gerado: {result}")
            
            if os.path.exists(result):
                size = os.path.getsize(result)
                print(f"📁 Tamanho: {size} bytes")
                print(f"🎵 Duração estimada: ~{size/32000:.1f} segundos")
                print("\n🎧 Escute o arquivo para verificar se os nomes estão sendo pronunciados corretamente!")
            
        except Exception as e:
            print(f"❌ Erro ao gerar áudio: {str(e)}")
    
    print("\n" + "="*50)
    print("COMO USAR:")
    print("1. Adicione seus nomes no dicionário 'nomes_personalizados' acima")
    print("2. Execute este script para testar")
    print("3. Ajuste as pronúncias conforme necessário")
    print("4. Quando estiver satisfeito, adicione os nomes ao arquivo principal")
    print("="*50)

def adicionar_nome_interativo():
    """
    Função interativa para adicionar novos nomes.
    """
    print("\n=== ADICIONAR NOVO NOME ===")
    
    nome_original = input("Digite o nome original: ").strip()
    if not nome_original:
        print("Nome não pode estar vazio!")
        return
    
    print(f"\nComo '{nome_original}' deve ser pronunciado?")
    print("Exemplos:")
    print("- Kanzime → Canzimi")
    print("- Xerath → Xérat") 
    print("- Zythara → Zitára")
    
    pronuncia = input("Digite a pronúncia melhorada: ").strip()
    if not pronuncia:
        print("Pronúncia não pode estar vazia!")
        return
    
    # Criar texto de teste
    texto_teste = f"O herói {nome_original} partiu em sua jornada. {nome_original} era conhecido por sua coragem."
    
    print(f"\nTeste com '{nome_original}' → '{pronuncia}':")
    
    nomes_teste = {nome_original: pronuncia}
    texto_processado = preprocess_text_for_tts(texto_teste, nomes_teste)
    
    print(f"Antes: {texto_teste}")
    print(f"Depois: {texto_processado}")
    
    # Confirmar se quer gerar áudio
    gerar = input("\nGerar áudio de teste? (s/n): ").lower().strip()
    
    if gerar in ['s', 'sim', 'y', 'yes']:
        try:
            class DummySelf:
                pass
            
            output_file = f"teste_{nome_original.lower()}.mp3"
            result = convert_text_to_speech(DummySelf(), texto_teste, output_file)
            print(f"✅ Áudio gerado: {result}")
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    print(f"\n📝 Para adicionar permanentemente, adicione esta linha ao dicionário:")
    print(f"    '{nome_original}': '{pronuncia}',")

if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Testar nomes personalizados predefinidos")
    print("2. Adicionar novo nome interativamente")
    
    opcao = input("Digite 1 ou 2: ").strip()
    
    if opcao == "1":
        testar_pronucia_personalizada()
    elif opcao == "2":
        adicionar_nome_interativo()
    else:
        print("Opção inválida!") 
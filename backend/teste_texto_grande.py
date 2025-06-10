import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tasks.audiobook import convert_text_to_speech, preprocess_text_for_tts

# Texto de teste grande (simulando o problema do usuário)
texto_grande = """
CAPÍTULO 9
OS SETE PRISIONEIROS ILUSTRES DE KANZIME

Os Belfs mantinham dezenas de soldados na parte de cima de um imenso Penhasco conhecido como Arighon. Ele era coberto por uma rocha grossa que, quando vista de longe, parecia um imenso caldeirão virado de cabeça para baixo. Para chegar ao topo daquele penhasco havia apenas uma trilha íngreme e tortuosa, que era vigiada constantemente pelos soldados Belfs. Era praticamente impossível subir por ali sem ser visto pelos sentinelas que faziam rondas dia e noite.

Mas havia outra maneira de chegar ao topo do penhasco: por meio de uma caverna subterrânea que se estendia por quilômetros e quilômetros através das entranhas da montanha. Essa caverna era conhecida apenas pelos moradores mais antigos da região, aqueles que viveram por décadas naquelas terras e guardavam os segredos ancestrais. Mesmo assim, poucos se aventuravam a explorá-la devido aos perigos ocultos em suas profundezas sombrias.

No topo do penhasco, os Belfs construíram uma fortaleza impenetrável que se erguia como uma sentinela sombria contra o céu. Era lá que mantinham seus prisioneiros mais importantes - aqueles que possuíam informações valiosas sobre estratégias militares, rotas comerciais secretas, ou que representavam algum valor estratégico significativo nas negociações diplomáticas entre as nações em conflito.

Entre esses prisioneiros estavam sete figuras ilustres de Kanzime: dois generais experientes do exército real, um diplomata de alta patente com conexões em várias cortes, um comerciante extremamente rico com redes de negócios internacionais, um inventor genial conhecido por suas criações revolucionárias, uma sacerdotisa respeitada que dominava antigas artes místicas, e um jovem nobre com conexões importantes nas mais altas esferas da sociedade.

Cada um deles tinha sido capturado em circunstâncias diferentes e dramáticas, mas todos compartilhavam o mesmo destino sombrio: estavam presos na fortaleza do penhasco Arighon, vivendo em celas escuras e úmidas, aguardando um resgate que talvez nunca viesse ou uma libertação que parecia cada vez mais distante com o passar dos dias.

O general Markus era conhecido em todo o reino por sua estratégia brilhante e havia liderado várias vitórias importantes e decisivas para Kanzime contra seus inimigos. Suas táticas inovadoras e sua capacidade de inspirar os soldados o tornaram uma lenda viva. Sua captura foi um golpe devastador para o moral do exército e para a confiança do povo na capacidade de defesa do reino.

A sacerdotisa Lyra possuía conhecimentos antigos e profundos sobre magia ancestral e rituais sagrados que eram transmitidos de geração em geração. Os Belfs acreditavam fervorosamente que ela poderia revelar segredos místicos extremamente valiosos, incluindo fórmulas de poções mágicas e encantamentos poderosos que poderiam mudar o curso da guerra.

O inventor Theo tinha desenvolvido várias máquinas revolucionárias e dispositivos engenhosos que poderiam mudar drasticamente o curso da guerra e da história. Seus projetos inovadores eram cobiçados pelos inimigos, que sabiam do potencial devastador de suas criações. Entre suas invenções estavam catapultas melhoradas, armaduras mais resistentes e até mesmo protótipos de máquinas voadoras.

O diplomata Viktor possuía informações cruciais sobre alianças secretas e tratados confidenciais entre diferentes nações. Seu conhecimento sobre as relações internacionais e sua rede de contatos em várias cortes reais o tornavam uma fonte inestimável de informações estratégicas.

O comerciante Aldric controlava rotas comerciais vitais e conhecia segredos sobre a economia de várias nações. Suas riquezas eram enormes e sua influência se estendia por continentes inteiros. Os Belfs esperavam usar seu conhecimento para desestabilizar a economia inimiga.

O jovem nobre Edmund tinha conexões diretas com a família real e conhecia segredos da corte que poderiam ser usados como armas políticas devastadoras. Apesar de sua juventude, sua posição social lhe dava acesso a informações que outros jamais poderiam obter.

Cada prisioneiro representava uma peça importante e valiosa no grande jogo de poder que se desenrolava entre as nações, um tabuleiro complexo onde cada movimento podia decidir o destino de milhares de pessoas. E todos eles esperavam silenciosamente, dia após dia, por uma oportunidade de escape que parecia cada vez mais improvável, mantendo viva apenas a esperança de que alguém viesse em seu socorro antes que fosse tarde demais.

As condições na prisão eram deploráveis. Os prisioneiros eram mantidos em celas individuais, com apenas um pequeno buraco no teto para entrada de luz. A comida era escassa e de péssima qualidade, consistindo principalmente de pão duro e água turva. O frio da montanha penetrava nas pedras da fortaleza, tornando as noites um tormento de tremores e desconforto.

Apesar das adversidades, os sete prisioneiros não perderam completamente a esperança. Eles sabiam que suas capturas tinham sido um golpe significativo para Kanzime, mas também acreditavam que o reino não os abandonaria. Secretamente, eles planejavam uma fuga coordenada, aproveitando seus conhecimentos únicos e habilidades especiais para encontrar uma maneira de escapar da fortaleza aparentemente impenetrável.

A fuga seria perigosa e complexa, exigindo timing perfeito e cooperação total entre todos os prisioneiros. Mas eles estavam determinados a recuperar sua liberdade e retornar para casa, onde poderiam usar seus conhecimentos e habilidades para ajudar Kanzime em sua luta contra os invasores Belfs.
""".strip()

print("=== TESTE DE TEXTO GRANDE ===")
print(f"Tamanho do texto: {len(texto_grande)} caracteres")
print(f"Tamanho em bytes: {len(texto_grande.encode('utf-8'))} bytes")

# Testar pré-processamento
print("\n--- Testando pré-processamento ---")
texto_processado = preprocess_text_for_tts(texto_grande)
print(f"Texto processado - bytes: {len(texto_processado.encode('utf-8'))}")

# Testar TTS melhorado
print("\n--- Testando TTS melhorado ---")
class DummySelf:
    pass

output_file = "teste_texto_grande_melhorado.mp3"
try:
    print("Iniciando geração de áudio...")
    result = convert_text_to_speech(DummySelf(), texto_grande, output_file)
    print(f"✅ Áudio gerado com sucesso: {result}")
    
    if os.path.exists(result):
        size = os.path.getsize(result)
        print(f"Tamanho do arquivo gerado: {size} bytes")
        print(f"Duração estimada: ~{size/32000:.1f} segundos") # Estimativa rough
    else:
        print("❌ Arquivo não foi criado")
        
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE CONCLUÍDO ===")
print("Por favor, abra o arquivo gerado para verificar a qualidade da narração!") 
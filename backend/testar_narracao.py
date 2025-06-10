import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tasks.audiobook import convert_text_to_speech

# Texto de teste
texto_teste = """
Olá! Este é um teste da funcionalidade de narração.
Se você está ouvindo esta mensagem, significa que o Google Cloud Text-to-Speech está funcionando corretamente.
Esta é a voz de alta qualidade em português brasileiro.
"""

print("Testando a função de narração...")
try:
    # Criar um objeto dummy para simular o self
    class DummySelf:
        pass
    
    dummy = DummySelf()
    output_file = "teste_narracao_direta.mp3"
    
    result = convert_text_to_speech(dummy, texto_teste, output_file)
    print(f"✅ Narração gerada com sucesso: {result}")
    print("Por favor, abra o arquivo 'teste_narracao_direta.mp3' para verificar a narração.")
    
except Exception as e:
    print(f"❌ Erro ao gerar narração: {str(e)}")
    import traceback
    traceback.print_exc() 
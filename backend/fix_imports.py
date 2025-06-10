import os
import re

def fix_imports_in_file(filepath):
    """Corrige os imports em um arquivo Python"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir backend.app por app
    new_content = re.sub(r'from backend\.app', 'from app', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Corrigido: {filepath}")
        return True
    return False

def fix_all_imports():
    """Percorre todos os arquivos Python e corrige os imports"""
    fixed_count = 0
    
    for root, dirs, files in os.walk('app'):
        # Ignorar __pycache__
        if '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_imports_in_file(filepath):
                    fixed_count += 1
    
    print(f"\n🎉 Total de arquivos corrigidos: {fixed_count}")

if __name__ == "__main__":
    print("🔧 Corrigindo imports de 'backend.app' para 'app'...\n")
    fix_all_imports() 
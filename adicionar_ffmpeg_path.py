import os
import subprocess
import sys

print("Adicionando FFmpeg ao PATH do sistema...")

ffmpeg_path = r"C:\ffmpeg\bin"

# Verificar se o diretório existe
if not os.path.exists(ffmpeg_path):
    print(f"Erro: O diretório {ffmpeg_path} não foi encontrado!")
    sys.exit(1)

# Comando PowerShell para adicionar ao PATH do usuário
ps_command = f'''
$oldPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($oldPath -notlike "*{ffmpeg_path}*") {{
    $newPath = $oldPath + ";{ffmpeg_path}"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "FFmpeg adicionado ao PATH com sucesso!"
}} else {{
    Write-Host "FFmpeg já está no PATH!"
}}
'''

try:
    # Executar comando PowerShell
    result = subprocess.run(
        ["powershell", "-Command", ps_command],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    # Atualizar PATH da sessão atual
    current_path = os.environ.get('PATH', '')
    if ffmpeg_path not in current_path:
        os.environ['PATH'] = current_path + ';' + ffmpeg_path
        print("\nPATH atualizado para a sessão atual!")
    
    print("\n✓ Configuração concluída!")
    print("\nTestando FFmpeg...")
    
    # Testar FFmpeg
    test_result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    if test_result.returncode == 0:
        print("✓ FFmpeg está funcionando!")
        print("\nVersão instalada:")
        print(test_result.stdout.split('\n')[0])
    else:
        print("⚠ FFmpeg não está acessível. Reinicie o PowerShell e tente novamente.")
        
except Exception as e:
    print(f"Erro: {e}")
    print("\nAlternativa manual:")
    print("1. Pressione Win+X e selecione 'Sistema'")
    print("2. Clique em 'Configurações avançadas do sistema'")
    print("3. Clique em 'Variáveis de Ambiente'")
    print("4. Em 'Variáveis do usuário', selecione 'Path' e clique em 'Editar'")
    print(f"5. Adicione: {ffmpeg_path}")
    print("6. Clique OK em todas as janelas") 
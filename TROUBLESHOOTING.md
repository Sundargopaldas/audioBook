# 🚨 Guia de Solução de Problemas - AudioBook AI

## ❓ "Não está carregando" - Diagnóstico

### 🔍 **Passo 1: Identificar o Problema**

Marque onde está travando:

- [ ] **GitHub**: Não consegue aceitar convite ou acessar repositório
- [ ] **Clone**: Erro ao fazer `git clone`
- [ ] **Dependências**: Erro no `pip install` ou `npm install`
- [ ] **Execução**: Erro ao rodar `SISTEMA_COMPLETO.bat`
- [ ] **Navegador**: Site não carrega (localhost:3000)
- [ ] **Funcionalidade**: Upload de arquivo não funciona

### 🛠️ **Soluções por Problema**

#### 📌 **Problema: GitHub/Convite**
```bash
# Verificar acesso ao repositório
https://github.com/Sundargopaldas/audioBook

# Se não conseguir acessar:
# 1. Verificar email (incluindo spam)
# 2. Verificar notificações: https://github.com/notifications
# 3. Pedir para reenviar convite
```

#### 📌 **Problema: Clone do Repositório**
```bash
# Tentar clone HTTPS
git clone https://github.com/Sundargopaldas/audioBook.git

# Se der erro de autenticação:
# 1. Verificar se Git está instalado: git --version
# 2. Configurar Git:
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

#### 📌 **Problema: Dependências Backend**
```bash
# Verificar Python
python --version  # Deve ser 3.10+

# Se Python não estiver instalado:
# Download: https://www.python.org/downloads/

# Instalar dependências
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Se der erro de venv:
pip install virtualenv
python -m virtualenv venv
```

#### 📌 **Problema: Dependências Frontend**
```bash
# Verificar Node.js
node --version  # Deve ser 16+
npm --version

# Se Node.js não estiver instalado:
# Download: https://nodejs.org/

# Instalar dependências
cd frontend
npm install

# Se der erro, limpar cache:
npm cache clean --force
rm -rf node_modules
npm install
```

#### 📌 **Problema: Execução do Projeto**
```bash
# Método 1: Script automático
SISTEMA_COMPLETO.bat

# Método 2: Manual
# Terminal 1:
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Terminal 2:
cd frontend
npm start
```

#### 📌 **Problema: Navegador**
```bash
# URLs para testar:
# Backend API: http://localhost:8001/docs
# Frontend: http://localhost:3000

# Se não carregar:
# 1. Verificar se os serviços estão rodando
# 2. Verificar portas 8001 e 3000 livres
# 3. Desativar antivírus/firewall temporariamente
```

#### 📌 **Problema: Google Cloud Credentials**
```bash
# Você precisa criar suas próprias credenciais:
# 1. Acesse: https://console.cloud.google.com/
# 2. Crie projeto ou use existente
# 3. Habilite: Cloud Text-to-Speech API
# 4. Crie: Service Account Key (JSON)
# 5. Baixe e renomeie para: google-tts-key.json
# 6. Coloque na raiz do projeto
```

### 🔧 **Comandos de Diagnóstico**

#### **Verificar Instalações:**
```bash
# Verificar versões
python --version
node --version
npm --version
git --version

# Verificar se está no diretório correto
pwd  # Linux/Mac
cd  # Windows
```

#### **Verificar Serviços Rodando:**
```bash
# Windows - verificar portas em uso
netstat -an | find "8001"
netstat -an | find "3000"

# Se portas estiverem em uso, matar processos:
taskkill /f /im python.exe
taskkill /f /im node.exe
```

#### **Logs para Debug:**
```bash
# Logs do Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Logs do Frontend
cd frontend
npm start

# Copie TODA a mensagem de erro e envie!
```

### 📱 **Como Reportar Problemas**

**Template para reportar erro:**
```
🚨 ERRO ENCONTRADO:

📍 Etapa: [Ex: Executando backend]
💻 Sistema: [Windows/Linux/Mac]
🐍 Python: [Versão]
📦 Node.js: [Versão]

📝 Comando executado:
[Cole o comando aqui]

❌ Erro exato:
[Cole toda a mensagem de erro aqui]

📸 Print (se possível):
[Anexe screenshot]
```

### 🆘 **Contato para Suporte**

- **GitHub Issues**: Crie uma issue no repositório
- **Email**: Responda o email do convite
- **LinkedIn**: Mensagem direta

### ✅ **Teste Final**

Quando tudo estiver funcionando:

1. ✅ Backend rodando: http://localhost:8001/docs
2. ✅ Frontend rodando: http://localhost:3000
3. ✅ Upload de arquivo .txt funciona
4. ✅ Áudio é gerado e pode ser ouvido

---

💡 **Dica**: Use `SISTEMA_COMPLETO.bat` - ele automatiza quase tudo! 
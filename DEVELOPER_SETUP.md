# Guia de Configuração para Desenvolvedores - AudioBook AI

## 🏁 Setup Rápido para Novos Desenvolvedores

### 1. Pré-requisitos
- **Python 3.10+** (recomendado: 3.11)
- **Node.js 16+** e npm
- **Git** instalado
- **Conta Google Cloud** com API Text-to-Speech habilitada

### 2. Clonando o Repositório
```bash
git clone https://github.com/Sundargopaldas/audioBook.git
cd audioBook
```

### 3. Configuração das Credenciais Google Cloud

#### Obter Credenciais:
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Habilite a API "Cloud Text-to-Speech"
4. Vá em "Credenciais" > "Criar Credenciais" > "Chave de Conta de Serviço"
5. Baixe o arquivo JSON

#### Configurar no Projeto:
```bash
# Renomeie o arquivo baixado para google-tts-key.json
# Coloque na raiz do projeto
cp /caminho/para/suas/credenciais.json ./google-tts-key.json
```

### 4. Setup do Backend

```bash
# Navegue para a pasta backend
cd backend

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente (opcional)
cp .env.example .env  # Se existir
```

### 5. Setup do Frontend

```bash
# Em outro terminal, navegue para frontend
cd frontend

# Instale dependências
npm install

# Configure variáveis de ambiente (se necessário)
cp .env.example .env.local  # Se existir
```

### 6. Executando o Projeto

#### Opção 1: Script Automático (Windows)
```bash
# Na raiz do projeto
SISTEMA_COMPLETO.bat
```

#### Opção 2: Manual
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
npm start
```

### 7. Testando a Instalação

1. Acesse http://localhost:3000
2. Faça upload de um arquivo de teste (TXT, PDF ou DOCX)
3. Verifique se o áudio é gerado corretamente

## 🛠️ Estrutura do Projeto

```
audioBook/
├── backend/                 # API FastAPI
│   ├── app/                # Código principal da API
│   │   ├── api/           # Endpoints da API
│   │   ├── core/          # Configurações e segurança
│   │   ├── crud/          # Operações de banco de dados
│   │   ├── db/            # Configuração do banco
│   │   ├── models/        # Modelos SQLAlchemy
│   │   ├── schemas/       # Schemas Pydantic
│   │   └── tasks/         # Processamento de audiobooks
│   ├── requirements.txt   # Dependências Python
│   └── main.py           # Ponto de entrada
├── frontend/               # Interface React
│   ├── src/              # Código fonte React
│   ├── public/           # Arquivos públicos
│   └── package.json      # Dependências Node.js
├── google-tts-key.json    # Credenciais Google Cloud
├── README.md             # Documentação principal
└── SISTEMA_COMPLETO.bat  # Script de inicialização
```

## 🔧 Ferramentas de Desenvolvimento

### Scripts Úteis
- `SISTEMA_COMPLETO.bat` - Inicia backend + frontend
- `INICIAR_BACKEND_8001.bat` - Apenas backend
- `TESTAR_FRONTEND_REACT.bat` - Apenas frontend
- `TESTAR_SISTEMA_MELHORADO.bat` - Testes completos

### IDEs Recomendadas
- **Backend**: PyCharm, VS Code com Python Extension
- **Frontend**: VS Code com React/TypeScript Extensions

### Extensões VS Code Recomendadas
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.flake8",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next"
    ]
}
```

## 🧪 Testes

### Testes Backend
```bash
cd backend
pytest
```

### Testes Frontend
```bash
cd frontend
npm test
```

### Teste Manual Rápido
1. Execute `TESTAR_SISTEMA.bat`
2. Abra `testar_narracao_simples.html`
3. Teste upload e conversão

## 🐛 Debugging

### Logs do Backend
- Logs aparecem no console onde o uvicorn está rodando
- Arquivos de log em `backend/logs/` (se configurado)

### Debugging Frontend
- Use DevTools do navegador (F12)
- Console mostra erros de API e React

### Problemas Comuns

1. **Erro de credenciais Google Cloud**
   ```
   Solução: Verificar se google-tts-key.json está na raiz
   ```

2. **Porta em uso**
   ```
   Solução: SISTEMA_COMPLETO.bat mata processos automaticamente
   ```

3. **Dependências não instaladas**
   ```
   Solução: Reexecutar pip install -r requirements.txt e npm install
   ```

## 🚀 Deploy

### Desenvolvimento
- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- Docs API: http://localhost:8001/docs

### Produção (TODO)
- Configurar variáveis de ambiente de produção
- Setup de banco de dados PostgreSQL
- Configuração de CORS para domínio de produção

## 📞 Suporte

- **Issues**: Use o GitHub Issues para reportar bugs
- **Discussões**: Use GitHub Discussions para dúvidas
- **Código**: Siga as convenções de commit do projeto

## 🤝 Contribuindo

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

💡 **Dica**: Para desenvolvimento mais rápido, use `SISTEMA_COMPLETO.bat` que automatiza todo o processo! 
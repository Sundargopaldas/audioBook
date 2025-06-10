# Audiobook AI - Sistema de Conversão de Texto para Áudio com IA

Sistema completo para converter documentos (PDF, DOCX, TXT) em audiobooks usando Google Cloud Text-to-Speech com voz de alta qualidade em português brasileiro.

## 🚀 Recursos

- ✅ Upload de arquivos PDF, DOCX e TXT
- ✅ Extração automática de texto
- ✅ Conversão para áudio usando Google Cloud TTS
- ✅ Voz de alta qualidade: `pt-BR-Chirp3-HD-Achernar`
- ✅ Interface web moderna em React
- ✅ API REST com FastAPI
- ✅ Processamento em tempo real

## 📋 Pré-requisitos

- Python 3.10+
- Node.js 16+
- Credenciais do Google Cloud (arquivo `google-tts-key.json`)

## 🔧 Instalação

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend
```bash
cd frontend
npm install
```

## ▶️ Como Executar

### Opção 1: Script Automático (Recomendado)
Simplesmente execute o arquivo:
```
SISTEMA_COMPLETO.bat
```

### Opção 2: Manual

#### Backend:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### Frontend:
```bash
cd frontend
npm start
```

## 🎯 Como Usar

1. Execute `SISTEMA_COMPLETO.bat`
2. O navegador abrirá automaticamente em http://localhost:3000
3. Faça upload de um arquivo TXT, PDF ou DOCX
4. Aguarde o processamento
5. Ouça ou baixe o áudio gerado!

## 🧪 Testes

Para testar apenas a narração:
1. Execute `INICIAR_SERVIDOR_E_BACKEND.bat`
2. Abra `testar_narracao_simples.html` no navegador

## 🛠️ Configuração

- **Voz**: Configurada em `backend/app/tasks/audiobook.py`
- **Credenciais Google**: Arquivo `google-tts-key.json` na raiz

## 📁 Estrutura do Projeto

```
audiobook-ai/
├── backend/           # API FastAPI
├── frontend/          # Interface React
├── google-tts-key.json # Credenciais Google Cloud
├── SISTEMA_COMPLETO.bat # Script para iniciar tudo
└── README.md          # Este arquivo
```

## 🚨 Solução de Problemas

- **Porta em uso**: O script fecha automaticamente processos anteriores
- **Erro de CORS**: Já configurado para localhost:8001 e localhost:3000
- **Erro de autenticação**: O sistema cria um usuário de teste automaticamente

## 📝 Notas

- O sistema está configurado para desenvolvimento local
- Os arquivos de áudio são salvos em `backend/audiobooks_local/`
- Para produção, configure variáveis de ambiente apropriadas

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.celery_app import celery_app
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretório para arquivos estáticos se não existir
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Servir arquivos estáticos (áudios gerados)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Criar diretório para áudios se não existir
# Usar caminho absoluto para garantir que está correto
audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audiofiles"))
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

print(f"[INFO] Servindo arquivos de áudio de: {audio_dir}")

# Servir arquivos de áudio
app.mount("/audiofiles", StaticFiles(directory=audio_dir), name="audiofiles")

# Incluir rotas da API
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Audiobook AI"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "celery": celery_app.control.inspect().active()
    }

# Rota para servir arquivos MP3 diretamente (compatibilidade com URLs antigas)
@app.get("/{filename:path}")
async def serve_mp3(filename: str):
    if filename.endswith('.mp3'):
        # Tentar encontrar o arquivo em vários locais
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", filename),
            os.path.join(os.path.dirname(__file__), "..", "..", "audiofiles", filename),
            os.path.join(os.path.dirname(__file__), "..", "static", filename),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return FileResponse(path, media_type="audio/mpeg")
    
    # Servir páginas HTML de teste
    elif filename.endswith('.html'):
        html_path = os.path.join(os.path.dirname(__file__), "..", "..", filename)
        if os.path.exists(html_path):
            return FileResponse(html_path, media_type="text/html")
        
    return {"detail": "Not Found"}
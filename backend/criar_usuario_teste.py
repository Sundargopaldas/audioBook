import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.crud.users import users
from app.schemas.user import UserCreate

def criar_usuario_teste():
    db = SessionLocal()
    
    # Verificar se usuário já existe
    existing_user = users.get_by_email(db, email="test@example.com")
    if existing_user:
        print("Usuário de teste já existe!")
        return
    
    # Criar novo usuário
    user_data = UserCreate(
        email="test@example.com",
        password="test123",
        full_name="Usuário Teste"
    )
    
    try:
        users.create(db, obj_in=user_data)
        print("✅ Usuário de teste criado com sucesso!")
        print("Email: test@example.com")
        print("Senha: test123")
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    criar_usuario_teste() 
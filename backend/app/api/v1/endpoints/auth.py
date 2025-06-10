from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserLogin, UserResponse

from app.crud.users import users
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.deps import get_db
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = users.create(db, obj_in=user_in)
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/test-user")
def create_test_user(db: Session = Depends(get_db)):
    """
    Cria um usuário de teste e retorna o token - APENAS PARA DESENVOLVIMENTO
    """
    from app.models.user import User
    
    # Verificar se usuário de teste já existe
    test_user = db.query(User).filter(User.email == "test@example.com").first()
    
    if not test_user:
        # Criar usuário de teste com senha hasheada corretamente
        test_user = User(
            email="test@example.com",
            full_name="Usuário Teste",
            hashed_password=get_password_hash("test123")
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
    
    # Gerar token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": test_user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    } 
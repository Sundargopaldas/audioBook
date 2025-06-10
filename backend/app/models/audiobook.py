from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base  # Alterado

class Audiobook(Base):
    __tablename__ = "audiobook"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    status = Column(String(50), index=True)  # processing, completed, error
    progress = Column(Float, default=0)
    current_step = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    audio_url = Column(String(255), nullable=True)
    
    # Novos campos para melhor rastreamento
    text_content = Column(Text, nullable=True)  # Primeiros caracteres do texto extraído
    file_path = Column(String(500), nullable=True)  # Caminho do arquivo de áudio final
    original_file_path = Column(String(500), nullable=True)  # Caminho do arquivo original enviado
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="audiobooks")
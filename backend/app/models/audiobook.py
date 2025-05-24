from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Audiobook(Base):
    __tablename__ = "audiobook"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    status = Column(String(50), index=True)  # processing, completed, error
    progress = Column(Float, default=0)
    current_step = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    audio_url = Column(String(255), nullable=True)
    
    # Relacionamentos
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="audiobooks") 
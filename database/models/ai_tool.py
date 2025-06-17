from sqlalchemy import Column, String, Text, Boolean, Numeric, JSON
from sqlalchemy.orm import relationship
from database.sqlalchemy_config import Base
from database.models.base import BaseModel

class AITool(Base, BaseModel):
    """Modelo de ferramentas de IA"""
    __tablename__ = 'ai_tools'
    
    # Informações básicas
    name = Column(String(100), nullable=False, unique=True)
    url = Column(Text, nullable=False)
    description = Column(Text)
    category = Column(String(50), index=True)
    
    # Metadados
    tags = Column(JSON, default=list)
    rating = Column(Numeric(3, 2), default=0.0)
    is_featured = Column(Boolean, default=False)
    
    # Relacionamentos
    favorites = relationship("UserFavorite", back_populates="ai_tool", cascade="all, delete-orphan")
    
    def add_tag(self, tag: str):
        """Adiciona uma tag à ferramenta"""
        if self.tags is None:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove uma tag da ferramenta"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.sqlalchemy_config import Base
from database.models.base import BaseModel

class BrowserSettings(Base, BaseModel):
    __tablename__ = 'browser_settings'
    
    user_id = Column(String(36), ForeignKey('users.id'), unique=True, nullable=False)
    anti_detection_settings = Column(JSON, default=dict)
    cache_settings = Column(JSON, default=dict)
    language = Column(String(10), default='pt_BR')
    theme = Column(String(20), default='dark')
    privacy_settings = Column(JSON, default=dict)
    
    # Relacionamento
    user = relationship("User", back_populates="browser_settings", uselist=False)
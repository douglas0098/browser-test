from sqlalchemy import Column, String, Numeric, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.sqlalchemy_config import Base
from database.models.base import BaseModel

class Payment(Base, BaseModel):
    __tablename__ = 'payments'
    
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(Enum('pix', 'boleto', 'credit_card'))
    status = Column(Enum('pending', 'confirmed', 'cancelled', 'refunded'), default='pending')
    payment_details = Column(JSON)
    
    # Relacionamento
    user = relationship("User", back_populates="payments")
from sqlalchemy import Column, String, Enum, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from database.sqlalchemy_config import Base
from database.models.base import BaseModel
import hashlib

class User(Base, BaseModel):
    """Modelo de usuário do sistema"""
    __tablename__ = 'users'
    
    # Campos básicos
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    
    # Informações pessoais
    name = Column(String(100), nullable=False)
    cpf = Column(String(20), unique=True, nullable=True)  # nullable=True para testes
    phone = Column(String(20), unique=True, nullable=False, index=True)
    avatar_url = Column(Text)
    
    # Tipo e status da conta
    account_type = Column(
        Enum('admin', 'equipe', 'membro', 'convidado', 'avulso'),
        default='membro'
    )
    status = Column(
        Enum('active', 'inactive', 'suspended'),
        default='active'
    )
    
    # Timestamps especiais
    last_login = Column(DateTime)
    
    # Configurações do perfil em JSON
    profile_settings = Column(JSON, default=dict)
    
    def set_password(self, password: str):
        """Define a senha do usuário com hash"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verifica se a senha está correta"""
        return self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @property
    def is_active(self):
        """Verifica se o usuário está ativo"""
        return self.status == 'active'

    @property
    def first_name(self):
        """Retorna o primeiro nome"""
        return self.name.split()[0] if self.name else ""
    
    @property
    def last_name(self):
        """Retorna o sobrenome"""
        parts = self.name.split()
        return " ".join(parts[1:]) if len(parts) > 1 else ""

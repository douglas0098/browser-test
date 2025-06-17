from typing import Optional, Tuple, List
from datetime import datetime, timezone
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from database.models.user import User
from database.models.user_favorite import UserFavorite
from crud.base_manager import BaseManager

class SQLAlchemyUserManager(BaseManager[User]):
    """Manager específico para usuários usando SQLAlchemy"""
    
    def __init__(self):
        super().__init__(User)
    
    def register_user(self, username: str, password: str, email: str, 
                     name: str, phone: str, cpf: str = None,
                     account_type: str = 'membro') -> Tuple[bool, str]:
        """Registra um novo usuário com validações completas"""
        session = self.get_session()
        try:
            # 🔍 Verificações de unicidade
            
            # Verificar username ou email
            existing_user = session.query(User).filter(
                or_(User.username == username, User.email == email)
            ).first()
            if existing_user:
                if existing_user.username == username:
                    return False, "Nome de usuário já existe"
                else:
                    return False, "Email já cadastrado"
            
            # Verificar telefone único
            existing_phone = session.query(User).filter(User.phone == phone).first()
            if existing_phone:
                return False, "Telefone já cadastrado"
            
            # Verificar CPF se fornecido
            if cpf and cpf.strip():
                existing_cpf = session.query(User).filter(User.cpf == cpf).first()
                if existing_cpf:
                    return False, "CPF já cadastrado"
            
            # ✅ Validações de formato
            if not self._validate_phone(phone):
                return False, "Formato de telefone inválido"
            
            if not self._validate_email(email):
                return False, "Formato de email inválido"
            
            if len(password) < 6:
                return False, "Senha deve ter pelo menos 6 caracteres"
            
            if len(name.strip()) < 2:
                return False, "Nome deve ter pelo menos 2 caracteres"
            
            # 🆕 Criar novo usuário
            user = User(
                username=username,
                email=email,
                name=name.strip(),
                phone=self._clean_phone(phone),
                cpf=cpf.strip() if cpf and cpf.strip() else None,
                account_type=account_type
            )
            user.set_password(password)

            session.add(user)
            session.commit()

            print(f"✅ Usuário registrado: {username} ({name}) - Tel: {phone}")
            return True, user.id

        except Exception as e:
            session.rollback()
            self.logger.error(f"Erro ao registrar usuário: {e}")
            return False, f"Erro interno: {str(e)}"
        finally:
            session.close()

    def verify_login(self, username_or_email: str, password: str) -> Tuple[bool, str]:
        """Verifica credenciais de login"""
        session = self.get_session()
        try:
            # Buscar usuário por username ou email
            user = session.query(User).filter(
                or_(
                    User.username == username_or_email,
                    User.email == username_or_email
                )
            ).first()
            
            if not user:
                return False, "Usuário não encontrado"
            
            if not user.is_active:
                return False, "Usuário inativo"
            
            if not user.verify_password(password):
                return False, "Senha incorreta"
            
            # Atualizar último login
            user.last_login = datetime.now(timezone.utc)
            session.commit()
            
            return True, user.id
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Erro ao verificar login: {e}")
            return False, str(e)
        finally:
            session.close()
    
    def get_user_with_favorites(self, user_id: str) -> Optional[User]:
        """Busca usuário com seus favoritos carregados"""
        session = self.get_session()
        try:
            user = session.query(User).filter(
                User.id == user_id
            ).options(
                joinedload(User.favorites).joinedload(UserFavorite.ai_tool)
            ).first()
            
            return user
        finally:
            session.close()
    
    # 🛠️ Métodos auxiliares de validação
    
    def _validate_phone(self, phone: str) -> bool:
        """Valida formato do telefone"""
        # Remove caracteres não numéricos
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Telefone brasileiro: 10 ou 11 dígitos (com DDD)
        return len(clean_phone) in [10, 11]
    
    def _validate_email(self, email: str) -> bool:
        """Validação básica de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _clean_phone(self, phone: str) -> str:
        """Limpa e formata telefone"""
        # Remove tudo exceto números
        clean = ''.join(filter(str.isdigit, phone))
        
        # Formatar para padrão brasileiro
        if len(clean) == 11:  # Celular com 9
            return f"({clean[:2]}) {clean[2:7]}-{clean[7:]}"
        elif len(clean) == 10:  # Fixo
            return f"({clean[:2]}) {clean[2:6]}-{clean[6:]}"
        else:
            return phone  # Retorna original se não conseguir formatar
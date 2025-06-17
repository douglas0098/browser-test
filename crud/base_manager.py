from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.sqlalchemy_config import db_config
from database.models.base import BaseModel
import logging

# Type variable para modelos
ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseManager(Generic[ModelType]):
    """Manager base com operações CRUD comuns"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.logger = logging.getLogger(f"{__name__}.{model.__name__}")
    
    def get_session(self) -> Session:
        """Obtém uma sessão do banco"""
        return db_config.get_session()
    
    def create(self, **kwargs) -> Optional[ModelType]:
        """Cria um novo registro"""
        session = self.get_session()
        try:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Erro ao criar {self.model.__name__}: {e}")
            return None
        finally:
            session.close()
    
    def get_by_id(self, id: str) -> Optional[ModelType]:
        """Busca por ID"""
        session = self.get_session()
        try:
            return session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao buscar {self.model.__name__}: {e}")
            return None
        finally:
            session.close()
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Lista todos os registros com paginação"""
        session = self.get_session()
        try:
            return session.query(self.model).limit(limit).offset(offset).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao listar {self.model.__name__}: {e}")
            return []
        finally:
            session.close()
    
    def update(self, id: str, **kwargs) -> bool:
        """Atualiza um registro"""
        session = self.get_session()
        try:
            instance = session.query(self.model).filter(self.model.id == id).first()
            if not instance:
                return False
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Erro ao atualizar {self.model.__name__}: {e}")
            return False
        finally:
            session.close()
    
    def delete(self, id: str) -> bool:
        """Remove um registro"""
        session = self.get_session()
        try:
            instance = session.query(self.model).filter(self.model.id == id).first()
            if not instance:
                return False
            
            session.delete(instance)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Erro ao deletar {self.model.__name__}: {e}")
            return False
        finally:
            session.close()
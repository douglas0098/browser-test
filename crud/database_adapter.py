# crud/database_adapter.py
from crud.sqlalchemy_user_manager import SQLAlchemyUserManager
from crud.sqlalchemy_ai_tools_manager import SQLAlchemyAIToolsManager
from database.sqlalchemy_config import db_config
from sqlalchemy import text

class DatabaseAdapter:
    """Adaptador para manter compatibilidade com código existente"""
    
    def __init__(self):
        # Usar os novos managers SQLAlchemy
        self.users = SQLAlchemyUserManager()
        self.ai_tools = SQLAlchemyAIToolsManager()
        # ... outros managers
    
    def is_connected(self) -> bool:
        """Verifica conexão com banco"""
        try:
            # Tenta executar uma query simples
            session = db_config.get_session()
            result = session.execute(text("SELECT 1 as test"))
            session.close()
            print("✅ Verificação de conexão bem-sucedida")
            return True
        except:
            return False
    
    def get_status(self):
        """Retorna status do sistema"""
        return {
            "database_connected": self.is_connected(),
            "managers_loaded": {
                "users": self.users is not None,
                "ai_tools": self.ai_tools is not None,
                # ... outros
            }
        }

# Substituir o crud_system existente
crud_system = DatabaseAdapter()
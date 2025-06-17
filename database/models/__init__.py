# 1. Importar configuração base
from database.sqlalchemy_config import Base
from database.models.base import BaseModel

# 2. Importar modelos individuais (sem relacionamentos)
from database.models.user import User
from database.models.ai_tool import AITool
from database.models.user_favorite import UserFavorite
from database.models.payment import Payment
from database.models.browser_settings import BrowserSettings
from database.models.user_session import UserSession
from database.models.download import Download

# 3. Configurar relacionamentos após todos os modelos estarem carregados
from database.models.relationships import *

# 4. Exportar todos
__all__ = [
    'Base',
    'BaseModel',
    'User',
    'AITool',
    'UserFavorite',
    'Payment',
    'BrowserSettings',
    'UserSession',
    'Download'
]
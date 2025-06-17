from sqlalchemy.orm import relationship
from database.models.user import User
from database.models.ai_tool import AITool
from database.models.user_favorite import UserFavorite
from database.models.payment import Payment
from database.models.browser_settings import BrowserSettings
from database.models.user_session import UserSession
from database.models.download import Download

# Adicionar relacionamentos ao User
User.favorites = relationship(
    "UserFavorite", 
    back_populates="user", 
    cascade="all, delete-orphan"
)

User.payments = relationship(
    "Payment", 
    back_populates="user", 
    cascade="all, delete-orphan"
)

User.browser_settings = relationship(
    "BrowserSettings", 
    back_populates="user", 
    uselist=False,
    cascade="all, delete-orphan"
)

User.sessions = relationship(
    "UserSession", 
    back_populates="user", 
    cascade="all, delete-orphan"
)

User.downloads = relationship(
    "Download", 
    back_populates="user", 
    cascade="all, delete-orphan"
)

# Adicionar relacionamentos ao AITool
AITool.favorites = relationship(
    "UserFavorite", 
    back_populates="ai_tool", 
    cascade="all, delete-orphan"
)

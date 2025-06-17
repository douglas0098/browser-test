# crud/sqlalchemy_ai_tools_manager.py
from typing import List, Optional, Tuple
from sqlalchemy import and_, or_
from database.models.ai_tool import AITool
from crud.base_manager import BaseManager

class SQLAlchemyAIToolsManager(BaseManager[AITool]):
    """Manager para ferramentas de IA usando SQLAlchemy"""
    
    def __init__(self):
        super().__init__(AITool)
    
    def add_tool(self, name: str, url: str, description: str, 
                 category: str, tags: List[str], is_featured: bool = False) -> Tuple[bool, str]:
        """Adiciona nova ferramenta de IA"""
        session = self.get_session()
        try:
            # Verificar se já existe
            existing = session.query(AITool).filter(
                or_(AITool.name == name, AITool.url == url)
            ).first()
            
            if existing:
                return False, "Ferramenta já existe"
            
            # Criar nova ferramenta
            tool = AITool(
                name=name,
                url=url,
                description=description,
                category=category,
                tags=tags,
                is_featured=is_featured
            )
            
            session.add(tool)
            session.commit()
            
            return True, tool.id
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Erro ao adicionar ferramenta: {e}")
            return False, str(e)
        finally:
            session.close()
    
    def get_by_category(self, category: str, limit: int = 50) -> List[AITool]:
        """Busca ferramentas por categoria"""
        session = self.get_session()
        try:
            return session.query(AITool).filter(
                AITool.category == category
            ).order_by(
                AITool.is_featured.desc(),
                AITool.rating.desc()
            ).limit(limit).all()
        finally:
            session.close()
    
    def search_tools(self, query: str) -> List[AITool]:
        """Busca ferramentas por nome ou descrição"""
        session = self.get_session()
        try:
            search_term = f"%{query}%"
            return session.query(AITool).filter(
                or_(
                    AITool.name.ilike(search_term),
                    AITool.description.ilike(search_term)
                )
            ).all()
        finally:
            session.close()
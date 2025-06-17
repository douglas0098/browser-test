# database/sqlalchemy_config.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Base para todos os modelos
Base = declarative_base()

class DatabaseConfig:
    """Configuração centralizada do banco de dados"""
    
    def __init__(self):
        self.DATABASE_URL = self._get_database_url()
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _get_database_url(self):
        """Constrói a URL de conexão do banco"""
        # CORREÇÃO: Garantir que o formato está correto
        # Formato: mysql+pymysql://user:password@host:port/database
        
        # Valores padrão
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', 'ProjetoBrowser2025')
        host = os.getenv('DB_HOST', '127.0.0.1')
        port = os.getenv('DB_PORT', '3308')
        database = os.getenv('DB_NAME', 'browser')
        
        # Construir URL manualmente para evitar problemas
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        
        print(f"Conectando com: mysql+pymysql://{user}:****@{host}:{port}/{database}")
        
        return url
    
    def _initialize_engine(self):
        """Inicializa o engine do SQLAlchemy com pool de conexões"""
        try:
            self.engine = create_engine(
                self.DATABASE_URL,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600,
                echo=False,  # True para debug
                # Adicionar charset
                connect_args={
                    'charset': 'utf8mb4'
                }
            )
            
            # Testar conexão
            with self.engine.connect() as conn:
                print("✅ Conexão com banco estabelecida via SQLAlchemy!")
            
            # Criar session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            raise
    
    def get_session(self):
        """Retorna uma nova sessão do banco"""
        return self.SessionLocal()
    
    def create_tables(self):
        """Cria todas as tabelas no banco"""
        Base.metadata.create_all(bind=self.engine)

# Instância global da configuração
db_config = DatabaseConfig()
#!/usr/bin/env python3
"""
Script para resetar o banco de dados durante desenvolvimento
"""

import os
import sys
from sqlalchemy import text

def reset_database():
    """Dropa todas as tabelas e recria o esquema"""
    print("🗄️ Script de Reset do Banco de Dados")
    print("⚠️  ATENÇÃO: Isso irá DELETAR TODOS OS DADOS!")
    
    confirm = input("Tem certeza que deseja continuar? (digite 'SIM' para confirmar): ")
    if confirm != 'SIM':
        print("❌ Operação cancelada")
        return
    
    try:
        # Importar configuração do banco
        from database.sqlalchemy_config import db_config, Base
        
        print("\n1. 🔌 Conectando ao banco...")
        engine = db_config.engine
        
        print("2. 🗑️ Dropando todas as tabelas...")
        
        # Obter sessão
        session = db_config.get_session()
        
        # Desabilitar verificação de chaves estrangeiras temporariamente
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Lista de tabelas para dropar (na ordem correta)
        tables_to_drop = [
            'user_favorites',
            'user_sessions', 
            'payments',
            'browser_settings',
            'downloads',
            'ai_tools',
            'users',
            'alembic_version'  # Tabela do Alembic também
        ]
        
        for table in tables_to_drop:
            try:
                session.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"   ✅ Tabela '{table}' removida")
            except Exception as e:
                print(f"   ⚠️  Erro ao remover '{table}': {e}")
        
        # Reabilitar verificação de chaves estrangeiras
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        session.commit()
        session.close()
        
        print("\n3. 🏗️ Recriando tabelas com novo esquema...")
        
        # Recriar todas as tabelas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Todas as tabelas recriadas com sucesso!")
        
        print("\n4. 👤 Criando usuário administrativo padrão...")
        
        # Importar sistema CRUD
        from crud.database_adapter import crud_system
        
        # Criar usuário admin padrão
        success, result = crud_system.users.register_user(
            username="admin",
            password="admin123",
            email="admin@upbrowser.com",
            name="Administrador do Sistema",
            phone="(11) 99999-0000",
            cpf="000.000.000-00"
        )
        
        if success:
            print("   ✅ Usuário admin criado (admin/admin123)")
        else:
            print(f"   ⚠️  Erro ao criar admin: {result}")
        
        # Criar usuário de teste
        success, result = crud_system.users.register_user(
            username="browser_test",
            password="test123",
            email="browser@test.com",
            name="Usuário de Teste",
            phone="(11) 99999-1111"
        )
        
        if success:
            print("   ✅ Usuário de teste criado (browser_test/test123)")
        else:
            print(f"   ⚠️  Erro ao criar teste: {result}")
        
        print("\n🎉 Reset completo! Banco de dados pronto para usar.")
        print("\n📋 Usuários disponíveis:")
        print("   - admin / admin123 (Administrador)")
        print("   - browser_test / test123 (Teste)")
        
    except Exception as e:
        print(f"\n❌ Erro durante reset: {e}")
        import traceback
        traceback.print_exc()

def show_current_tables():
    """Mostra as tabelas atuais no banco"""
    try:
        from database.sqlalchemy_config import db_config
        from sqlalchemy import text
        
        session = db_config.get_session()
        result = session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
        session.close()
        
        print("\n📋 Tabelas atuais no banco:")
        if tables:
            for table in tables:
                print(f"   - {table}")
        else:
            print("   (Nenhuma tabela encontrada)")
            
    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")

def main():
    print("🗄️ Gerenciador de Reset do Banco - UP Browser")
    
    while True:
        print("\n" + "="*50)
        print("Escolha uma opção:")
        print("1. 🗑️  Reset completo (dropar + recriar)")
        print("2. 📋 Mostrar tabelas atuais")
        print("3. ❌ Sair")
        
        choice = input("\nDigite sua escolha (1-3): ").strip()
        
        if choice == "1":
            reset_database()
            
        elif choice == "2":
            show_current_tables()
            
        elif choice == "3":
            print("👋 Saindo...")
            break
            
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
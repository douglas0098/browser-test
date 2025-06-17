import os
import sys

# Configurar ambiente
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox"
os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_OPENGL"] = "software"


def main():
    """Função principal"""
    print("🚀 UP Browser - Iniciando sistema...")

    # 1. Verificar sistema CRUD
    print("\n1. Verificando sistema CRUD...")
    try:
        from crud.database_adapter import crud_system
        
        # Teste de conexão mais detalhado
        if crud_system.is_connected():
            print("   ✅ CRUD conectado ao banco")
            
            # 2. Criar usuário de teste se não existir (COM NOVOS CAMPOS)
            print("\n2. Preparando dados de teste...")
            success, result = crud_system.users.register_user(
                username="browser_test",
                password="test123",
                email="browser@test.com",
                name="Usuário de Teste",  # ← NOVO
                phone="(11) 99999-9999",   # ← NOVO
                cpf="123.456.789-00"       # ← OPCIONAL
            )
            if success:
                print("   ✅ Usuário de teste criado")
            else:
                print(f"   ℹ️  Usuário já existe ou erro: {result}")
        else:
            print("   ⚠️  Banco de dados offline - algumas funcionalidades limitadas")
            
    except Exception as e:
        print(f"   ❌ Erro no sistema CRUD: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Iniciar navegador
    print("\n3. Iniciando navegador...")
    try:
        from core.app import run_browser
        print("   🎯 Navegador iniciando...")
        run_browser()
    except KeyboardInterrupt:
        print("\n\n👋 Navegador fechado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
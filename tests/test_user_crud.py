import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crud.crud_manager import crud_system

class TestUserCRUD(unittest.TestCase):
    """Testes para operações CRUD de usuários"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.user_manager = crud_system.users
        self.test_username = "test_user_crud"
        self.test_email = "test@crud.com"
        self.test_password = "test123"
    
    def test_01_register_user(self):
        """Teste: Registrar novo usuário"""
        print("\n🧪 Testando registro de usuário...")
        
        success, result = self.user_manager.register_user(
            username=self.test_username,
            password=self.test_password,
            email=self.test_email,
            name="Usuário Teste"
        )
        
        print(f"Resultado: {success}, {result}")
        self.assertTrue(success, f"Falha ao registrar usuário: {result}")
        self.test_user_id = result
    
    def test_02_verify_login(self):
        """Teste: Verificar login do usuário"""
        print("\n🧪 Testando login de usuário...")
        
        success, result = self.user_manager.verify_login(
            self.test_username, 
            self.test_password
        )
        
        print(f"Login resultado: {success}, {result}")
        self.assertTrue(success, f"Falha no login: {result}")
    
    def test_03_get_user_by_id(self):
        """Teste: Buscar usuário por ID"""
        print("\n🧪 Testando busca de usuário por ID...")
        
        # Primeiro, fazer login para obter o ID
        success, user_id = self.user_manager.verify_login(
            self.test_username, 
            self.test_password
        )
        
        if success:
            user_data = self.user_manager.get_user_by_id(user_id)
            print(f"Dados do usuário: {user_data}")
            self.assertIsNotNone(user_data, "Usuário não encontrado")
            self.assertEqual(user_data['username'], self.test_username)
    
    def test_04_update_user(self):
        """Teste: Atualizar dados do usuário"""
        print("\n🧪 Testando atualização de usuário...")
        
        # Obter ID do usuário
        success, user_id = self.user_manager.verify_login(
            self.test_username, 
            self.test_password
        )
        
        if success:
            update_data = {
                "name": "Nome Atualizado",
                "whatsapp": "(11) 99999-9999"
            }
            
            result = self.user_manager.update_user(user_id, update_data)
            print(f"Atualização resultado: {result}")
            self.assertTrue(result, "Falha ao atualizar usuário")
    
    def test_05_list_users(self):
        """Teste: Listar todos os usuários"""
        print("\n🧪 Testando listagem de usuários...")
        
        users = self.user_manager.list_all_users(limit=10)
        print(f"Usuários encontrados: {len(users)}")
        
        self.assertIsInstance(users, list, "Deve retornar uma lista")
        
        # Verificar se nosso usuário de teste está na lista
        test_user_found = any(user['username'] == self.test_username for user in users)
        self.assertTrue(test_user_found, "Usuário de teste não encontrado na lista")

if __name__ == "__main__":
    unittest.main(verbosity=2)
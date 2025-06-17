import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crud.crud_manager import crud_system

class TestAIToolsCRUD(unittest.TestCase):
    """Testes para operações CRUD de ferramentas de IA"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.ai_tools_manager = crud_system.ai_tools
        self.test_tool_data = {
            "name": "ChatGPT Test",
            "url": "https://chat.openai.com/test",
            "description": "Ferramenta de teste para IA conversacional",
            "category": "conversacao",
            "tags": ["teste", "conversacao", "ia"]
        }
    
    def test_01_add_tool(self):
        """Teste: Adicionar nova ferramenta de IA"""
        print("\n🧪 Testando adição de ferramenta de IA...")
        
        success, result = self.ai_tools_manager.add_tool(
            name=self.test_tool_data["name"],
            url=self.test_tool_data["url"],
            description=self.test_tool_data["description"],
            category=self.test_tool_data["category"],
            tags=self.test_tool_data["tags"]
        )
        
        print(f"Resultado: {success}, ID: {result}")
        self.assertTrue(success, f"Falha ao adicionar ferramenta: {result}")
        self.test_tool_id = result
    
    def test_02_get_tool_by_id(self):
        """Teste: Buscar ferramenta por ID"""
        print("\n🧪 Testando busca de ferramenta por ID...")
        
        # Primeiro adicionar uma ferramenta
        success, tool_id = self.ai_tools_manager.add_tool(
            name="Teste Busca",
            url="https://teste.com",
            description="Teste",
            category="teste",
            tags=["teste"]
        )
        
        if success:
            tool_data = self.ai_tools_manager.get_tool_by_id(tool_id)
            print(f"Ferramenta encontrada: {tool_data}")
            self.assertIsNotNone(tool_data, "Ferramenta não encontrada")
            self.assertEqual(tool_data['name'], "Teste Busca")
    
    def test_03_list_all_tools(self):
        """Teste: Listar todas as ferramentas"""
        print("\n🧪 Testando listagem de ferramentas...")
        
        tools = self.ai_tools_manager.get_all_tools(limit=20)
        print(f"Ferramentas encontradas: {len(tools)}")
        
        self.assertIsInstance(tools, list, "Deve retornar uma lista")
        
        for tool in tools:
            self.assertIn('name', tool)
            self.assertIn('url', tool)
            self.assertIn('category', tool)
    
    def test_04_get_categories(self):
        """Teste: Obter categorias de ferramentas"""
        print("\n🧪 Testando obtenção de categorias...")
        
        categories = self.ai_tools_manager.get_tool_categories()
        print(f"Categorias encontradas: {categories}")
        
        self.assertIsInstance(categories, list, "Deve retornar uma lista")
    
    def test_05_update_tool(self):
        """Teste: Atualizar ferramenta"""
        print("\n🧪 Testando atualização de ferramenta...")
        
        # Primeiro adicionar uma ferramenta
        success, tool_id = self.ai_tools_manager.add_tool(
            name="Ferramenta Para Atualizar",
            url="https://update.com",
            description="Para atualizar",
            category="teste",
            tags=["teste"]
        )
        
        if success:
            update_data = {
                "description": "Descrição atualizada",
                "tags": ["teste", "atualizado"]
            }
            
            result = self.ai_tools_manager.update_tool(tool_id, update_data)
            print(f"Atualização resultado: {result}")
            self.assertTrue(result, "Falha ao atualizar ferramenta")

if __name__ == "__main__":
    unittest.main(verbosity=2)
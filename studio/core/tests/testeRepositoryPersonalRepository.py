from datetime import datetime
from unittest import TestCase
from bson import ObjectId
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo
from core.entity.PersonalEntity import PersonalEntity

class TestPersonalRepository(TestCase):
    def setUp(self):
        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo.mydb['mock_personal']
        self.repo = PersonalRepository(self.mongo)
        
        # Limpar dados de teste anteriores
        self.mongo._colecao.delete_many({"cpf": {"$in": ["111", "222", "333", "444"]}})

    def tearDown(self):
        # Limpar dados após cada teste
        self.mongo._colecao.delete_many({"cpf": {"$in": ["111", "222", "333", "444"]}})

    # Testes para criar()
    def test_criar_sucesso(self):
        personal_data = {
            "nome": "Carlos Trainer",
            "cpf": "111",
            "cref": "123456",
            "email": "carlos@academia.com",
            "telefone": "11987654321",
            "salario": 3000.00,
            "acesso": "admin"
        }
        personal = PersonalEntity(personal_data)
        
        # Garantir que não existe personal com mesmo CPF
        self.assertFalse(self.repo.consultarCpf("111"))
        
        result = self.repo.criar(personal)
        self.assertTrue(result)
        
        # Verificar se o personal foi criado
        personal_criado = self.repo.consultarCpf("111")
        self.assertIsNotNone(personal_criado)
        self.assertEqual(personal_criado["nome"], "Carlos Trainer")
        self.assertEqual(personal_criado["cref"], "123456")
        self.assertEqual(personal_criado["salario"], 3000.00)

    def test_criar_cpf_duplicado(self):
        personal_data = {
            "nome": "Carlos Trainer",
            "cpf": "111",
            "cref": "123456"
        }
        personal = PersonalEntity(personal_data)
        
        # Criar primeiro personal
        self.repo.criar(personal)
        
        # Tentar criar personal com mesmo CPF
        with self.assertRaises(Exception) as context:
            self.repo.criar(personal)
        
        self.assertIn("Esse personal já está cadastrado", str(context.exception))

    # Testes para consultarCpf()
    def test_consultarCpf_existente(self):
        personal_data = {
            "nome": "Ana Coach",
            "cpf": "222",
            "cref": "654321",
            "email": "ana@academia.com"
        }
        personal = PersonalEntity(personal_data)
        self.repo.criar(personal)
        
        result = self.repo.consultarCpf("222")
        self.assertIsNotNone(result)
        self.assertEqual(result["cpf"], "222")
        self.assertEqual(result["nome"], "Ana Coach")
        self.assertEqual(result["email"], "ana@academia.com")

    def test_consultarCpf_inexistente(self):
        result = self.repo.consultarCpf("00000000000")
        self.assertFalse(result)

    # Testes para deletarByCpf()
    def test_deletarByCpf_existente(self):
        personal_data = {
            "nome": "Pedro Instructor",
            "cpf": "333",
            "cref": "987654"
        }
        personal = PersonalEntity(personal_data)
        self.repo.criar(personal)
        
        result = self.repo.deletarByCpf("333")
        self.assertTrue(result)
        
        # Verificar se foi deletado
        self.assertFalse(self.repo.consultarCpf("333"))

    def test_deletarByCpf_inexistente(self):
        with self.assertRaises(Exception) as context:
            self.repo.deletarByCpf("00000000000")
        
        self.assertIn("CPF: 00000000000 não encontrado", str(context.exception))

    # Testes para listarTodos()
    def test_listarTodos(self):
        # Criar alguns personais
        personal1_data = {
            "nome": "Personal 1",
            "cpf": "111",
            "cref": "111111",
            "email": "personal1@academia.com"
        }
        
        personal2_data = {
            "nome": "Personal 2",
            "cpf": "222",
            "cref": "222222",
            "email": "personal2@academia.com"
        }
        
        self.repo.criar(PersonalEntity(personal1_data))
        self.repo.criar(PersonalEntity(personal2_data))
        
        result = list(self.repo.listarTodos())
        cpf_list = [p["cpf"] for p in result]
        self.assertIn("111", cpf_list)
        self.assertIn("222", cpf_list)
        self.assertEqual(len(result), 2)
        
        # Verificar dados completos
        personal1 = next(p for p in result if p["cpf"] == "111")
        self.assertEqual(personal1["nome"], "Personal 1")
        self.assertEqual(personal1["cref"], "111111")

    # Testes para consultarId()
    def test_consultarId_existente(self):
        personal_data = {
            "nome": "Mariana Trainer",
            "cpf": "444",
            "cref": "444444",
            "email": "mariana@academia.com"
        }
        personal = PersonalEntity(personal_data)
        self.repo.criar(personal)
        
        # Obter ID do documento criado
        personal_criado = self.repo.consultarCpf("444")
        personal_id = personal_criado["_id"]
        
        result = self.repo.consultarId(personal_id)
        self.assertIsNotNone(result)
        self.assertEqual(result["_id"], personal_id)
        self.assertEqual(result["nome"], "Mariana Trainer")
        self.assertEqual(result["email"], "mariana@academia.com")

    # Testes para atualizar()
    def test_atualizar_sucesso(self):
        # Criar personal
        personal_data = {
            "nome": "Carlos Trainer",
            "cpf": "111",
            "cref": "123456",
            "email": "carlos@old.com"
        }
        personal = PersonalEntity(personal_data)
        self.repo.criar(personal)
        
        # Atualizar personal
        personal_atualizado_data = {
            "nome": "Carlos Atualizado",
            "cpf": "111",
            "cref": "654321",
            "email": "carlos@new.com",
            "telefone": "11999999999",
            "salario": 4000.00
        }
        personal_atualizado = PersonalEntity(personal_atualizado_data)
        
        result = self.repo.atualizar(personal_atualizado)
        self.assertIsNotNone(result)
        
        # Verificar atualização
        personal_db = self.repo.consultarCpf("111")
        self.assertEqual(personal_db["nome"], "Carlos Atualizado")
        self.assertEqual(personal_db["cref"], "654321")
        self.assertEqual(personal_db["email"], "carlos@new.com")
        self.assertEqual(personal_db["telefone"], "11999999999")
        self.assertEqual(personal_db["salario"], 4000.00)

    # Testes para deletarById()
    def test_deletarById_sucesso(self):
        personal_data = {
            "nome": "Personal para Deletar",
            "cpf": "444",
            "cref": "444444"
        }
        personal = PersonalEntity(personal_data)
        self.repo.criar(personal)
        
        # Criar entidade apenas com CPF para deleção
        personal_deletar = PersonalEntity({"cpf": "444"})
        
        result = self.repo.deletarById(personal_deletar)
        self.assertTrue(result)
        
        # Verificar se foi deletado
        self.assertFalse(self.repo.consultarCpf("444"))

    # Teste para campos adicionais da PersonalEntity
    def test_criar_com_campos_completos(self):
        personal_data = {
            "nome": "Personal Completo",
            "senha": "senha123",
            "telefone": "11999999999",
            "email": "completo@academia.com",
            "cpf": "111",
            "salario": 3500.50,
            "acesso": "admin",
            "cref": "123456"
        }
        personal = PersonalEntity(personal_data)
        
        result = self.repo.criar(personal)
        self.assertTrue(result)
        
        # Verificar todos os campos
        personal_criado = self.repo.consultarCpf("111")
        self.assertEqual(personal_criado["nome"], "Personal Completo")
        self.assertEqual(personal_criado["senha"], "senha123")
        self.assertEqual(personal_criado["telefone"], "11999999999")
        self.assertEqual(personal_criado["email"], "completo@academia.com")
        self.assertEqual(personal_criado["salario"], 3500.50)
        self.assertEqual(personal_criado["acesso"], "admin")
        self.assertEqual(personal_criado["cref"], "123456")

    def __del__(self):
        self.mongo.mydb.drop_collection('mock_personal')
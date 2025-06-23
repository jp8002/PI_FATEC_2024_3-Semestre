
from datetime import datetime
from unittest import TestCase
from core.repositories.AlunoRepository import AlunoRepository
from core.entity.AlunoEntity import Aluno
from core.services.ConexaoMongo import ConexaoMongo

class TestAlunoRepository(TestCase):
    def setUp(self):
        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['mock']
        self.repo = AlunoRepository(self.mongo)
        
        # Limpar dados de teste anteriores
        self.mongo._colecao.delete_many({"cpf": {"$in": ["44", "00000000000", "66","77"]}})

    def tearDown(self):
        # Limpar dados após cada teste
        self.mongo._colecao.delete_many({"cpf": {"$in": ["44", "00000000000", "66","77"]}})

    # Testes para criar()
    def test_criar_sucesso(self):
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        
        # Garantir que não existe aluno com mesmo CPF
        self.assertFalse(self.repo.consultarCpf("44"))
        
        result = self.repo.criar(aluno)
        self.assertTrue(result)
        
        # Verificar se o aluno foi criado
        aluno_criado = self.repo.consultarCpf("44")
        self.assertIsNotNone(aluno_criado)
        self.assertEqual(aluno_criado["nome"], "João Silva")

    def test_criar_cpf_duplicado(self):
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        
        # Criar primeiro aluno
        self.repo.criar(aluno)
        
        # Tentar criar aluno com mesmo CPF
        with self.assertRaises(Exception) as context:
            self.repo.criar(aluno)
        
        self.assertIn("Um aluno com esse cpf já exite", str(context.exception))

    # Testes para consultarCpf()
    def test_consultarCpf_existente(self):
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        self.repo.criar(aluno)
        
        result = self.repo.consultarCpf("44")
        self.assertIsNotNone(result)
        self.assertEqual(result["cpf"], "44")
        self.assertEqual(result["nome"], "João Silva")

    def test_consultarCpf_inexistente(self):
        result = self.repo.consultarCpf("00000000000")
        self.assertFalse(result)

    # Testes para deletarByCpf()
    def test_deletarByCpf_existente(self):
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        self.repo.criar(aluno)
        
        result = self.repo.deletarByCpf("44")
        self.assertTrue(result)
        
        # Verificar se foi deletado
        self.assertFalse(self.repo.consultarCpf("44"))

    def test_deletarByCpf_inexistente(self):
        with self.assertRaises(Exception) as context:
            self.repo.deletarByCpf("00000000000")
        
        self.assertIn("CPF: 00000000000 não encontrado", str(context.exception))

    # Testes para listarTodos()
    def test_listarTodos(self):
        # Criar alguns alunos
        
        aluno1_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }

        aluno2_data = {
            "nome": "Maria Souza",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "66",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }



        self.repo.criar(Aluno(aluno1_data))
        self.repo.criar(Aluno(aluno2_data))
        
        result = self.repo.listarTodos()
        cpf_list = [aluno["cpf"] for aluno in result]
        self.assertIn("44", cpf_list)
        self.assertIn("66", cpf_list)

    # Testes para atualizar()
    def test_atualizar_sucesso(self):
        # Criar aluno
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        self.repo.criar(aluno)
        
        # Atualizar aluno
        aluno_atualizado_data = {
            "nome": "João Atualizado",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "atualizado@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno_atualizado = Aluno(aluno_atualizado_data)
        
        result = self.repo.atualizar(aluno_atualizado)
        self.assertIsNotNone(result)
        
        # Verificar atualização
        aluno_db = self.repo.consultarCpf("44")
        self.assertEqual(aluno_db["nome"], "João Atualizado")
        self.assertEqual(aluno_db["email"], "atualizado@example.com")

    # Testes para agendar()
    def test_agendar_sucesso(self):
        # Criar aluno
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        self.repo.criar(aluno)
        
        agendamento = {
            "cpf": "44",
            "data": "2024-01-01T10:00",
            "exercicios": ["Supino", "Agachamento"]
        }
        
        result = self.repo.agendar(agendamento)
        self.assertTrue(result)
        
        # Verificar se a sessão foi adicionada
        aluno_db = self.repo.consultarCpf("44")
        self.assertEqual(len(aluno_db["sessoes"]), 1)
        self.assertEqual(aluno_db["sessoes"][0]["exercicios"], ["Supino", "Agachamento"])

    def test_agendar_cpf_inexistente(self):
        agendamento = {
            "cpf": "00000000000",
            "data": "2024-01-01T10:00",
            "exercicios": ["Supino"]
        }
        
        with self.assertRaises(Exception) as context:
            self.repo.agendar(agendamento)
        
        self.assertIn("Esse cpf não existe", str(context.exception))

    # Testes para AlterarStatus()
    def test_AlterarStatus_para_ativo(self):
        # Criar aluno com status cancelado
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        self.repo.criar(aluno)
        
        result = self.repo.AlterarStatus("on", "44")
        self.assertTrue(result)
        
        # Verificar atualização
        aluno_db = self.repo.consultarCpf("44")
        self.assertEqual(aluno_db["status"], "Ativo")

    def test_AlterarStatus_para_cancelado(self):
        # Criar aluno com status ativo
        aluno_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }
        aluno = Aluno(aluno_data)
        self.repo.criar(aluno)
        
        result = self.repo.AlterarStatus("off", "44")
        self.assertTrue(result)
        
        # Verificar atualização
        aluno_db = self.repo.consultarCpf("44")
        self.assertEqual(aluno_db["status"], "Cancelado")

    # Testes para alunoPorPersonal()
    def test_alunoPorPersonal(self):
        # Criar alunos com diferentes personais

        aluno1_data = {
            "nome": "Maria Souza",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "66",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }

        aluno2_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "ativo",
            "sessoes": []
        }

        aluno3_data = {
            "nome": "Carlos Santos",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "77",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal B",
            "status": "ativo",
            "sessoes": []
        }
        
        self.repo.criar(Aluno(aluno1_data))
        self.repo.criar(Aluno(aluno2_data))
        self.repo.criar(Aluno(aluno3_data))
        
        result = self.repo.alunoPorPersonal("Personal Teste")
        self.assertEqual(len(result), 2)
        cpf_list = [aluno["cpf"] for aluno in result]
        self.assertIn("44", cpf_list)
        self.assertIn("66", cpf_list)
        self.assertNotIn("77", cpf_list)

    # Testes para métodos de agregação
    def test_TodosAlunosPorStatus(self):
        # Criar alunos com diferentes status

        aluno1_data = {
            "nome": "Maria Souza",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "66",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "Ativo",
            "sessoes": []
        }

        aluno2_data = {
            "nome": "João Silva",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "44",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal Teste",
            "status": "Ativo",
            "sessoes": []
        }

        aluno3_data = {
            "nome": "Carlos Santos",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "77",
            "telefone": "11999999999",
            "email": "joao@example.com",
            "plano": "mensal",
            "personal": "Personal B",
            "status": "Cancelado",
            "sessoes": []
        }

        
        self.repo.criar(Aluno(aluno1_data))
        self.repo.criar(Aluno(aluno2_data))
        self.repo.criar(Aluno(aluno3_data))
        
        result = self.repo.TodosAlunosPorStatus()
        status_counts = {item["_id"]: item["qtd"] for item in result}
        
        self.assertEqual(status_counts.get("Ativo", 0), 2)
        self.assertEqual(status_counts.get("Cancelado", 0), 1)
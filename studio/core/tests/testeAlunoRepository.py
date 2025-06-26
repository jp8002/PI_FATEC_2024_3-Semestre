
from django.test import TestCase

from datetime import datetime

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.ConexaoMongo import ConexaoMongo

class TestAlunoRepository(TestCase):
    def setUp(self):
        self.mongo = ConexaoMongo('localhost', '27017', "test_db")
        self.mongo._colecao = self.mongo.mydb['test_collection']
        self.repo = AlunoRepository(self.mongo)

        # Dados iniciais para os testes
        self.aluno_data = {
            "nome": "Carlos Silva",
            "data_nascimento": datetime(1990, 5, 15),
            "cpf": "12345678900",
            "status": "ativo",
            "telefone": "11999998888",
            "sessoes": [
                {"dia": datetime(2024, 6, 10, 10, 0), "exercicios": ["supino", "agachamento"]},
                {"dia": datetime(2024, 6, 15, 14, 0), "exercicios": ["corrida", "remada"]}
            ],
            "data_assinatura": "2024-01-01T08:00:00",
            "personal": "Personal A",
            "plano": "Premium",
            "idade": 34,
            "data_renovacao": "2024-02-01T08:00:00"
        }
        self.aluno_id = self.mongo._colecao.insert_one(self.aluno_data).inserted_id

        # Segundo aluno para testes de agrupamento
        self.mongo._colecao.insert_one({
            "nome": "Maria Oliveira",
            "cpf": "98765432100",
            "status": "inativo",
            "personal": "Personal B",
            "plano": "Básico",
            "idade": 28
        })

    def tearDown(self):
        self.mongo._colecao.drop()

    # TESTES EXISTENTES (modelo base)
    def test_criar_novo_aluno(self):
        novo = {
            "nome": "Novo Aluno",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "11122233344",
            "status": "ativo",
            "telefone": "11999997777"
        }
        aluno_entity = Aluno(novo)
        result = self.repo.criar(aluno_entity)
        self.assertTrue(result)
        
        # Verifica se realmente foi criado
        aluno_db = self.repo.consultarCpf("11122233344")
        self.assertEqual(aluno_db["nome"], "Novo Aluno")

    def test_consultarCpf(self):
        aluno = self.repo.consultarCpf("12345678900")
        self.assertEqual(aluno["nome"], "Carlos Silva")

    def test_deletarById(self):
        result = self.repo.deletarById(self.aluno_id)
        self.assertTrue(result)
        
        # Verifica se foi removido
        with self.assertRaises(Exception):
            self.repo.consultarId(self.aluno_id)

    def test_listarTodos(self):
        alunos = self.repo.listarTodos()
        self.assertEqual(len(alunos), 2)

    def test_atualizar(self):
        dados_atualizados = {
            "cpf": "12345678900",
            "nome": "Carlos Atualizado",
            "telefone": "11988887777"
        }
        aluno_entity = Aluno(dados_atualizados)
        result = self.repo.atualizar(aluno_entity)
        self.assertTrue(result)
        
        # Verifica atualização
        aluno_db = self.repo.consultarCpf("12345678900")
        self.assertEqual(aluno_db["nome"], "Carlos Atualizado")
        self.assertEqual(aluno_db["telefone"], "11988887777")

    def test_consultar_datas_agendadas(self):
        datas = self.repo.consultar_datas_agendadas()
        self.assertIn("01/01/2024", datas)

    def test_agendar(self):
        agendamento = {
            "cpf": "12345678900",
            "data": "2024-07-01T10:00",
            "exercicios": ["leg press", "cadeira flexora"]
        }
        result = self.repo.agendar(agendamento)
        self.assertTrue(result)
        
        # Verifica se foi adicionado
        aluno = self.repo.consultarCpf("12345678900")
        self.assertEqual(len(aluno["sessoes"]), 3)

    def test_deletarAgendamento(self):
        dia_str = "2024-06-10T10:00"
        result = self.repo.deletarAgendamento("12345678900", dia_str)
        self.assertTrue(result)
        
        # Verifica se foi removido
        aluno = self.repo.consultarCpf("12345678900")
        self.assertEqual(len(aluno["sessoes"]), 1)

    # NOVOS TESTES (métodos não cobertos)
    def test_deletarByCpf(self):
        result = self.repo.deletarByCpf("12345678900")
        self.assertTrue(result)
        
        # Verifica se foi removido
        aluno = self.repo.consultarCpf("12345678900")
        self.assertFalse(aluno)

    def test_consultarId(self):
        aluno = self.repo.consultarId(self.aluno_id)
        self.assertEqual(aluno["cpf"], "12345678900")

    def test_listarSessoes(self):
        sessoes = self.repo.listarSessoes("12345678900")
        self.assertEqual(len(sessoes["sessoes"]), 2)
        self.assertEqual(sessoes["nome"], "Carlos Silva")

    def test_listarSessaoPorDia(self):
        dia_str = "2024-06-10"
        sessao = self.repo.listarSessaoPorDia("12345678900", dia_str)
        self.assertEqual(len(sessao["sessoes"]), 1)
        self.assertEqual(sessao["sessoes"][0]["exercicios"], ["supino", "agachamento"])

    def test_atualizarAgendamento(self):
        agendamento = {
            "cpf": "12345678900",
            "dia": "2024-06-20T09:00",
            "exercicios": ["atualizado1", "atualizado2"],
            "idSessao": 0
        }
        result = self.repo.atualizarAgendamento(agendamento)
        self.assertTrue(result)
        
        # Verifica atualização
        aluno = self.repo.consultarCpf("12345678900")
        self.assertEqual(aluno["sessoes"][0]["exercicios"], ["atualizado1", "atualizado2"])
        self.assertEqual(aluno["sessoes"][0]["dia"], datetime(2024, 6, 20, 9, 0))

    def test_TodosAlunosPorStatus(self):
        result = self.repo.TodosAlunosPorStatus()
        status_counts = {item["_id"]: item["qtd"] for item in result}
        self.assertEqual(status_counts.get("ativo", 0), 1)
        self.assertEqual(status_counts.get("inativo", 0), 1)

    def test_TodosAlunosPorPersonal(self):
        result = self.repo.TodosAlunosPorPersonal()
        personal_counts = {item["_id"]: item["qtd"] for item in result}
        self.assertEqual(personal_counts.get("Personal A", 0), 1)
        self.assertEqual(personal_counts.get("Personal B", 0), 1)

    def test_TodosAlunosPorPlano(self):
        result = self.repo.TodosAlunosPorPlano()
        plano_counts = {item["_id"]: item["qtd"] for item in result}
        self.assertEqual(plano_counts.get("Premium", 0), 1)
        self.assertEqual(plano_counts.get("Básico", 0), 1)

    def test_alunoPorIdade(self):
        result = self.repo.alunoPorIdade()
        idades = {item["_id"]: item["qtd"] for item in result}
        self.assertEqual(idades.get(34, 0), 1)
        self.assertEqual(idades.get(28, 0), 1)

    def test_AlterarStatus(self):
        # Teste ativar
        result_ativar = self.repo.AlterarStatus("on", "98765432100")
        self.assertTrue(result_ativar)
        aluno = self.repo.consultarCpf("98765432100")
        self.assertEqual(aluno["status"], "Ativo")
        
        # Teste desativar
        result_desativar = self.repo.AlterarStatus("off", "98765432100")
        self.assertTrue(result_desativar)
        aluno = self.repo.consultarCpf("98765432100")
        self.assertEqual(aluno["status"], "Cancelado")

    def test_alunoPorPersonal(self):
        alunos = self.repo.alunoPorPersonal("Personal A")
        self.assertEqual(len(alunos), 1)
        self.assertEqual(alunos[0]["cpf"], "12345678900")
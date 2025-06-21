import ipdb
from django.test import TestCase

from core.entity.AlunoEntity import Aluno
from core.entity.PersonalEntity import PersonalEntity
from core.repositories.AlunoRepository import AlunoRepository
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo
from datetime import datetime

class TesteServiceMongo(TestCase):
    def setUp(self):
        self.mongo = ConexaoMongo('localhost', '27017', "mock")
        self.mongo._colecao = self.mongo._mydb['mockcol']

        self.alunoRepository = AlunoRepository(self.mongo)
        self.personalRepository = PersonalRepository(self.mongo)

        self.personalEntity = PersonalEntity({})
        self.alunoEntity = Aluno({})

        self.id = self.mongo._colecao.insert_one({"nome": "joao", "cpf": "123654789"})
        self.mongo._colecao.insert_one({"nome": "persona", "cpf": "12345678910"})

        self.mongo._colecao.insert_one({
            "status": "ativo",
            "data_assinatura": "2024-03-01T08:00:00"
        })
        self.mongo._colecao.insert_one({
            "status": "inativo",
            "data_assinatura": "2024-03-02T09:00:00"
        })


    def test_consultar_datas_agendadas(self):
        resp = self.alunoRepository.consultar_datas_agendadas()
        self.assertIn("01/03/2024", resp)
        self.assertNotIn("02/03/2024", resp)

    def test_consultarCpf(self):
        resp = self.alunoRepository.consultarCpf("123654789")
        self.assertEqual(resp.get("nome", "Não foi encontrado"), "joao")

    def test_criarNovoPersonal(self):
        Novo = {'nome':"Otavio", 'senha':"otavio123", 'telefone':"999999999", 'email':"otavio@gmail.com", 'cpf':"2",
                                            'salario':"1500", 'acesso':"funcionario", 'cref':"999999-P/SP"}

        self.personalEntity = PersonalEntity(Novo)

        resp = self.personalRepository.criar(self.personalEntity)

        self.assertTrue(resp)

    def test_criarNovoAluno(self):

        novo = {"nome": "joao mock", "data_nascimento": datetime(2002,2,1), "cpf": "1", "status": "ativo",
             "telefone": "123424564646"}

        self.alunoEntity = Aluno(novo)

        resp = self.alunoRepository.criar(self.alunoEntity)


        self.assertTrue(resp)

    def test_listaAlunos(self):
        resp = self.alunoRepository.listarTodos()
        # ipdb.set_trace()
        self.assertTrue(resp)

    def test_agendar(self):
        resp = self.alunoRepository.agendar({"cpf": "123654789", "dia": "2025-05-06T20:06",'exercicios':['coxa','perna']})
        self.assertTrue(resp)

    def test_deletarAgendamento(self):
        self.alunoRepository.agendar({"cpf": "123654789", "dia": "2025-05-06T20:06",'exercicios':['coxa','perna']})
        resp = self.alunoRepository.deletarAgendamento(cpf = "123654789", dia = "2025-05-06T20:06")
        self.assertTrue(resp)

    def test_listaPersonals(self):
        resp = self.personalRepository.listarTodos()

        self.assertTrue(resp)

    def test_editarPersonal(self):

        atualizar = { 'cpf' : "12345678910",
        'nome' : "mock peres",
        'cref' : "999999-P/SP",
        'telefone' : "912345678",
        'email' : "peres@mock.com",
        'salario' : 1600.0,
        'acesso' : "admin" }

        self.personalEntity = PersonalEntity(atualizar)

        resp = self.personalRepository.atualizar(self.personalEntity)

        self.assertTrue(resp)

        registro_atualizado = self.mongo._colecao.find_one({"cpf": "12345678910"})


        self.assertEqual(registro_atualizado["telefone"], "912345678")
        self.assertEqual(registro_atualizado["email"], "peres@mock.com")
        self.assertEqual(registro_atualizado["salario"], float("1600.0"))
        self.assertEqual(registro_atualizado["acesso"], "admin")
        self.assertEqual(registro_atualizado["nome"], "mock peres")
        self.assertEqual(registro_atualizado["cref"], "999999-P/SP")

    def test_editarAluno(self):

        self.alunoEntity = Aluno({"nome": "joao fake", "data_nascimento": "2019-10-27", "status": "ativo", "cpf": "123654789",
             "telefone": "963258741"})

        resp = self.alunoRepository.atualizar(self.alunoEntity)

        self.assertTrue(resp)

    def test_deletarAluno(self):
        id = self.mongo._colecao.insert_one({"cpf": "123654789", "nome": "tony fake"}).inserted_id

        resp = self.alunoRepository.deletarById(id)
        self.assertEqual(resp, True)

    def test_listarAlunosPorStatus(self):
        resp = self.alunoRepository.listarAlunosPorStatus("ativo")
        self.assertTrue(resp)

    def __del__(self):
        self.mongo._colecao.drop()

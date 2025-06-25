from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo

class TesteViewGerenciamentoAgendamentosPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key
        self.mongo = ConexaoMongo()

        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.insert_one({"nome": "Joana Costa", "senha": "joana123", "telefone": "(11) 91234-0001", "email": "joana.costa@academia.com", "salario": 3000, "cpf": "12333678910", "acesso": "adm", "cref": "123456-G/SP"})

        self.mongo._colecao = self.mongo.mydb['aluno']

        self.id = self.mongo._colecao.insert_one({"nome": "joao mock", "cpf": "12345678901", "senha": "1234", "sessoes":[]})

        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "12345678901", 'data': '2025-05-19T00:00','exercicios':['perna','coxa']})
        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "12345678901", 'data': '2025-06-19T00:00','exercicios':['perna','coxa']})
        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "12345678901", 'data': '2025-07-19T00:00','exercicios':['perna','coxa']})

    def test_excluir(self):
        self.resp = self.client.post(
            reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}),
            {'acao': 'Excluir', 'dia': '2025-05-19T00:00'}
        )
        self.assertEqual(self.resp.status_code, 302)

    def test_salvar(self):
        self.resp = self.client.post(
            reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}),
            {'acao': 'Salvar', 'dia': '2025-05-19T00:00', 'exercicios': 'perna', 'idSessao': '0'}
        )
        self.assertEqual(self.resp.status_code, 302)

    def test_filtrar(self):
        self.resp = self.client.post(
            reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}),
            {'acao': 'filtrar', 'dataEscolhida': '2025-05-19T00:00'}
        )

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':'12345678901'})
        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})
    
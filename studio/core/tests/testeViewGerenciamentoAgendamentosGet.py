from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo

class TesteViewGerenciamentoAgendamentosGet(TestCase):
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
        self.resp = self.client.get(reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateGerenciamentoTreinos.html")

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':'12345678901'})
        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})
    
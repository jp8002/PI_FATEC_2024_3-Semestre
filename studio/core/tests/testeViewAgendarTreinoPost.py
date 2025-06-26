
from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo


class TesteViewAgendarTreinoPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo.mydb['aluno']

        self.id = self.mongo._colecao.insert_one({"nome": "joao mock", "cpf": "123654789", "senha": "1234", "sessoes":[]})

        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "123654789", 'dia': '2025-05-19T00:00','exercicios':['perna','coxa']})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateAgendarTreino.html")

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':'123654789'})

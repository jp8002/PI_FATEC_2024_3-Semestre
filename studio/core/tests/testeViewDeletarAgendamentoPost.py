from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo


class TesteViewDeletarAgendamentoPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.mongo._colecao.update_one({"cpf" :"123456789"} ,{"$push": {"sessoes": "2025-05-19T00:00"}})
        self.id = self.mongo._colecao.insert_one({"nome" :"joao mock" ,"cpf" :"123456789" ,"senha" :"1234"})

        cpf = "123456789"
        dia = "2025-05-19T00:00"

        self.resp = self.client.post(reverse("deletarAgendamento") ,{ 'cpf': '123456789', 'dia': '2025-05-19T00:00'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateDeletarAgendamento.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':"123456789"})

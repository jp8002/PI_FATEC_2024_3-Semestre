from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo

class TesteViewDeletarAgendamentoGet(TestCase):
    def setUp(self):

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['personal']
        self.mongo._colecao.insert_one({"nome": "Joana Costa", "senha": "joana123", "telefone": "(11) 91234-0001", "email": "joana.costa@academia.com", "salario": 3000, "cpf": "12333678910", "acesso": "adm", "cref": "123456-G/SP"})


        self.resp = self.client.get(reverse("deletarAgendamento"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateDeletarAgendamento.html")

    def test_combobox(self):
        self.assertContains(self.resp,"<select")

    def __del__(self):
        self.mongo._colecao = self.mongo._mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})

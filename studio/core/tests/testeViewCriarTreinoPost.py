from bson import ObjectId
from django.test import TestCase
from django.urls import reverse

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.ConexaoMongo import ConexaoMongo


class TesteViewCriarTreinoPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']

        dados = {"nome": "joao mock", "cpf": "123654789", "senha": "1234",'treinos':[]}


        self.id = self.mongo._colecao.insert_one(dados).inserted_id

        self.resp = self.client.post(reverse("criarTreino") ,{ 'id': ObjectId(self.id), 'treino': 'Remada'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateCriarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo._colecao.delete_many({'id': ObjectId(self.id)})

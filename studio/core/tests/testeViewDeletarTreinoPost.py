import ipdb
from bson import ObjectId
from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo


class TesteViewDeletarTreinoPost(TestCase):

    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']

        dados ={
            "nome": "joao_mock_Deletar_Treino",
            "senha": "1234",
            "treinos": ["Remada"]
        }

        self.id = self.mongo._colecao.insert_one(dados)

        self.resp = self.client.post(reverse("deletarTreino") ,{ '_id': self.id.inserted_id, 'treino': 'Remada'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateDeletarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo._colecao.delete_many({'_id':ObjectId(self.id.inserted_id)})

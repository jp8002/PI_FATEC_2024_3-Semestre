from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo



class TesteViewCadastrarAlunoPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']

        aluno = {"nome": "joao mock", "data_nascimento": "2019-05-20", "cpf": "123456789", "telefone": "123456"}

        self.resp = self.client.post(reverse("cadastrarAluno"), aluno)

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_post(self):
        x = self.mongo._colecao.find_one({"cpf":"123456789"})
        self.assertEqual(x.get("nome", "Não foi possível encontrar"), "joao mock")

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateCadastrarAluno.html")

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':"123456789"})

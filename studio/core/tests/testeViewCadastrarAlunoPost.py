import ipdb
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

        aluno = {"nome": "joao mock", "data_nascimento": "2019-05-20", 'senha':'1234',"cpf": "1234567897867", "telefone": "123456",'email':'joaomock@gmail.com','plano':'trimestral','personal':'Joana Costa'}

        self.resp = self.client.post(reverse("cadastrarAluno"), aluno)

    def test_302_response(self):
        self.assertEqual(self.resp.status_code, 302)


    def test_post(self):
        x = self.mongo._colecao.find_one({"cpf":"1234567897867"})
        self.assertEqual(x.get("nome", "Não foi possível encontrar"), "Joao Mock")

    def test_template(self):

        self.assertRedirects(self.resp, reverse('cadastrarAluno'), status_code=302, target_status_code=200, fetch_redirect_response=True)

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':"1234567897867"})

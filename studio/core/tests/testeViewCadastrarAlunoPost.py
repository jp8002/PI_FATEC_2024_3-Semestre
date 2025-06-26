
from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo



class TesteViewCadastrarAlunoPost(TestCase):
    def setUp(self):
        self.mongo = ConexaoMongo()

        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.insert_one({"nome": "Joana Costa", "senha": "joana123", "telefone": "(11) 91234-0001", "email": "joana.costa@academia.com", "salario": 3000, "cpf": "12333678910", "acesso": "adm", "cref": "123456-G/SP"})


        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["acesso"] = "adm"
        sessao['cpf'] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        

        self.mongo._colecao = self.mongo.mydb['aluno']

    def test_302_response(self):
        aluno = {"nome": "joao mock", "data_nascimento": "2019-05-20", "cpf": "12345678999", "telefone": "123456",'email':'joaomock@gmail.com','plano':'Trimestral','personal':'Joana Costa'}
        self.resp = self.client.post(reverse("cadastrarAluno"), aluno)

        self.assertEqual(self.resp.status_code, 302)


    def test_post(self):
        aluno = {"nome": "joao mock", "cpf": "12345678977", "data_nascimento": "2019-05-20", "telefone": "123456",'email':'joaomock@gmail.com','plano':'Trimestral','personal':'Joana Costa'}
        self.resp = self.client.post(reverse("cadastrarAluno"), aluno)

        x = self.mongo._colecao.find_one({"cpf": "12345678977"})

        self.assertEqual(x.get("nome", "Não foi possível encontrar"), "Joao Mock")

    def test_template(self):
        aluno = {"nome": "joao mock", "data_nascimento": "2019-05-20", "cpf": "12345678978", "telefone": "123456",'email':'joaomock@gmail.com','plano':'Trimestral','personal':'Joana Costa'}
        self.resp = self.client.post(reverse("cadastrarAluno"), aluno)
        
        self.assertRedirects(self.resp, reverse('cadastrarAluno'), status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_nao_adm(self):
        self.client.session.flush()

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["acesso"] = "funcionario"
        sessao['cpf'] = "12333678"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        aluno = {"nome": "joao mock", "data_nascimento": "2019-05-20", "cpf": "12345678999", "telefone": "123456",'email':'joaomock@gmail.com','plano':'Trimestral','personal':'Joana Costa'}
        self.resp = self.client.post(reverse("cadastrarAluno"), aluno)

        self.assertEqual(self.resp.status_code, 302)
    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':"12345678978"})
        self.mongo._colecao.delete_many({'cpf':"12345678977"})
        self.mongo._colecao.delete_many({'cpf':"12345678999"})

        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})

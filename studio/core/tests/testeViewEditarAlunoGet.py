from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarAlunoForm
from datetime import datetime

class TesteViewEditarAlunoGet(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()

        self.mongo._colecao = self.mongo._mydb['personal']
        self.mongo._colecao.insert_one({"nome": "Joana Costa", "senha": "joana123", "telefone": "(11) 91234-0001", "email": "joana.costa@academia.com", "salario": 3000, "cpf": "12333678910", "acesso": "adm", "cref": "123456-G/SP"})

        self.mongo._colecao = self.mongo._mydb['aluno']

        aluno = {"nome": "joao mock", "data_nascimento": "2019-05-20", "cpf": "44", "telefone": "123456",'email':'joaomock@gmail.com','plano':'trimestral','personal':'Joana Costa'}
        self.client.post(reverse("cadastrarAluno"), aluno)

        # Fazer a requisição GET para a view
        self.resp = self.client.get(reverse('editarAluno', kwargs={'cpf': '44'}))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateEditarAluno.html")

    def test_form_no_contexto(self):
        self.assertIn('form', self.resp.context)
        self.assertIsInstance(self.resp.context['form'], CadastrarAlunoForm)

    def test_cpf_no_contexto(self):
        self.assertEqual(self.resp.context['cpf'], '44')

    def test_dados_iniciais_do_formulario(self):
        form = self.resp.context['form']
        self.aluno_cleaned_data = {
            'nome': 'Joao Mock',
            'cpf': '44',
            'email': 'joaomock@gmail.com',
            'telefone': '123456',
            'plano': 'Trimestral',
            'data_nascimento': datetime(2019, 5, 20, 0, 0)
        }

        self.assertEqual(form.initial['nome'], self.aluno_cleaned_data['nome'])
        self.assertEqual(form.initial['cpf'], self.aluno_cleaned_data['cpf'])
        self.assertEqual(form.initial['email'], self.aluno_cleaned_data['email'])
        self.assertEqual(form.initial['telefone'], self.aluno_cleaned_data['telefone'])
        self.assertEqual(form.initial['plano'], self.aluno_cleaned_data['plano'])
        self.assertEqual(form.initial['data_nascimento'], self.aluno_cleaned_data['data_nascimento'])

    def tearDown(self):
        # Limpar o banco de dados após cada teste
        self.mongo._colecao.delete_many({'cpf': '44'})

        self.mongo._colecao = self.mongo._mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})
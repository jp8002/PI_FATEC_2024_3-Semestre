from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarPersonalForm
from datetime import datetime

class TesteViewEditarAlunoGet(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['personal']

        personal = {"nome": "joao mock", "senha": "123", "cpf": "66", "telefone": "123356",'email':'joaomock@gmail.com','salario':"1000",'cref':'655321-G/SP','acesso':'funcionario'}
        
        self.client.post(reverse("cadastrarPersonal"), personal)

        # Fazer a requisição GET para a view
        self.resp = self.client.get(reverse('editarPersonal', kwargs={'cpf': '66'}))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateEditarPersonal.html")

    def test_form_no_contexto(self):
        self.assertIn('form', self.resp.context)
        self.assertIsInstance(self.resp.context['form'], CadastrarPersonalForm)

    def test_cpf_no_contexto(self):
        self.assertEqual(self.resp.context['cpf'], '66')

    def test_dados_iniciais_do_formulario(self):
        form = self.resp.context['form']
        self.aluno_cleaned_data = {
            'nome': 'joao mock',
            'cpf': '66',
            'email': 'joaomock@gmail.com',
            'telefone': '123356',
            'senha': '123',
            'cref': '655321-G/SP',
            'salario': 1000,
            'acesso': 'funcionario'
        }

        self.assertEqual(form.initial['nome'], self.aluno_cleaned_data['nome'])
        self.assertEqual(form.initial['cpf'], self.aluno_cleaned_data['cpf'])
        self.assertEqual(form.initial['email'], self.aluno_cleaned_data['email'])
        self.assertEqual(form.initial['telefone'], self.aluno_cleaned_data['telefone'])
        self.assertEqual(form.initial['senha'], self.aluno_cleaned_data['senha'])
        self.assertEqual(form.initial['cref'], self.aluno_cleaned_data['cref'])
        self.assertEqual(form.initial['acesso'], self.aluno_cleaned_data['acesso'])
        self.assertEqual(form.initial['salario'], self.aluno_cleaned_data['salario'])

    def tearDown(self):
        # Limpar o banco de dados após cada teste
        self.mongo._colecao.delete_many({'cpf': '66'})
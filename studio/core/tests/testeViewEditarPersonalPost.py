from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo
from datetime import datetime

class TesteViewEditarPersonalPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.insert_one({"nome": "Joana Costa", "senha": "joana123", "telefone": "(11) 91234-0001", "email": "joana.costa@academia.com", "salario": 3000, "cpf": "12333678910", "acesso": "adm", "cref": "123456-G/SP"})

        
        personal = {"nome": "joao mock", "senha": "123", "cpf": "66", "telefone": "123356",'email':'joaomock@gmail.com','salario':"1000",'cref':'666321-G/SP','acesso':'funcionario'}
        
        self.client.post(reverse("cadastrarPersonal"), personal)

        self.resp = self.client.post(reverse('editarPersonal', kwargs={'cpf': '66'}))

    def test_post_dados_validos(self):
        """Testa atualização bem-sucedida com dados válidos"""
        
        dados_atualizados = {
            'nome': 'João Atualizado',
            'cpf': '66',
            'email': 'atualizado@email.com',
            'telefone': '123356',
            'senha': '123',
            'cref': '655321-G/SP',
            'salario': 1000,
            'acesso': 'funcionario'
        }

        response = self.client.post(
            reverse('editarPersonal', kwargs={'cpf': '66'}),
            dados_atualizados
        )
        
        # Verifica redirecionamento
        self.assertRedirects(response, reverse('listarPersonal'))
        
        # Verifica atualização no banco
        aluno_atualizado = self.mongo._colecao.find_one({'cpf': '66'})
        self.assertEqual(aluno_atualizado['nome'], 'João Atualizado')
        self.assertEqual(aluno_atualizado['email'], 'atualizado@email.com')
        self.assertEqual(aluno_atualizado['telefone'], '123356')
        self.assertEqual(aluno_atualizado['cref'], '655321-G/SP')
        self.assertEqual(aluno_atualizado['salario'], 1000)
        self.assertEqual(aluno_atualizado['acesso'], 'funcionario')
        self.assertEqual(aluno_atualizado['cpf'], '66')

    def test_post_dados_invalidos(self):
        """Testa comportamento com dados inválidos no formulário"""
        dados_invalidos = {
            'nome': '',  # Campo obrigatório
            'cpf': '66',
            'email': 'email-invalido',  # Formato inválido
            'telefone': '',
            'plano': 'inexistente',  # Opção inválida
            'data_nascimento': 'data-invalida'  # Formato errado
        }
        
        response = self.client.post(
            reverse('editarPersonal', kwargs={'cpf': '66'}),
            dados_invalidos
        )
        
        # Verifica resposta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TemplateEditarPersonal.html")
        
        # Verifica erros no formulário
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('telefone', form.errors)
        self.assertIn('salario', form.errors)
        
        # Verifica se dados originais permanecem no banco
        aluno_banco = self.mongo._colecao.find_one({'cpf': '66'})
        self.assertEqual(aluno_banco['nome'], 'joao mock')

    def test_post_tipo_usuario_invalido(self):
        """Testa acesso com tipo de usuário não autorizado"""
        self.client.session.flush()
        # Configurar sessão como não personal
        sessao = self.client.session
        sessao["sessao"] = False
        sessao['cpf'] = "12345678901"
        sessao.save()
        self.client.cookies['sessionid'] = sessao.session_key
        
        response = self.client.post(
            reverse('editarPersonal', kwargs={'cpf': '66'}),
            {}
        )
        
        self.assertRedirects(response, reverse('paginaInicial'))

    def tearDown(self):
        # Limpar banco de dados
        self.mongo._colecao.delete_many({'cpf': '66'})
        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})
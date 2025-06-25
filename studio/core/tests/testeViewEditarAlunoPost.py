from django.test import TestCase
from django.urls import reverse
from core.services.ConexaoMongo import ConexaoMongo
from datetime import datetime

class TesteViewEditarAlunoPost(TestCase):
    def setUp(self):
        # Configurar sessão
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12333678910"
        sessao.save()
        self.client.cookies['sessionid'] = sessao.session_key

        # Configurar banco de dados
        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.insert_one({"nome": "Joana Costa", "senha": "joana123", "telefone": "(11) 91234-0001", "email": "joana.costa@academia.com", "salario": 3000, "cpf": "12333678910", "acesso": "adm", "cref": "123456-G/SP"})

        self.mongo._colecao = self.mongo.mydb['aluno']
        
        # Criar aluno inicial
        self.aluno_inicial = {
            "nome": "João Original",
            "data_nascimento": datetime(2000, 1, 1),
            "cpf": "55",
            "telefone": "111111",
            "email": "original@email.com",
            "plano": "mensal",
            "personal": "Joana Costa",
            "status": "Ativo",
            "sessoes": 10
        }
        self.mongo._colecao.insert_one(self.aluno_inicial.copy())

    def test_post_dados_validos(self):
        """Testa atualização bem-sucedida com dados válidos"""
        
        dados_atualizados = {
            'nome': 'João Atualizado',
            'cpf': '55',
            'email': 'atualizado@email.com',
            'telefone': '999999',
            'plano': 'anual',
            'data_nascimento': '1999-12-31',
            'personal': 'Joana Costa'  # Personal existente
        }

        response = self.client.post(
            reverse('editarAluno', kwargs={'cpf': '55'}),
            dados_atualizados
        )
        
        # Verifica redirecionamento
        self.assertRedirects(response, reverse('listarAlunos'))
        
        # Verifica atualização no banco
        aluno_atualizado = self.mongo._colecao.find_one({'cpf': '55'})
        self.assertEqual(aluno_atualizado['nome'], 'João Atualizado')
        self.assertEqual(aluno_atualizado['email'], 'atualizado@email.com')
        self.assertEqual(aluno_atualizado['telefone'], '999999')
        self.assertEqual(aluno_atualizado['plano'], 'Anual')
        self.assertEqual(aluno_atualizado['data_nascimento'], datetime(1999, 12, 31))
        
        # Verifica campos preservados
        self.assertEqual(aluno_atualizado['status'], 'Ativo')
        self.assertEqual(aluno_atualizado['sessoes'], 10)

    def test_post_dados_invalidos(self):
        """Testa comportamento com dados inválidos no formulário"""
        dados_invalidos = {
            'nome': '',  # Campo obrigatório
            'cpf': '55',
            'email': 'email-invalido',  # Formato inválido
            'telefone': '',
            'plano': 'inexistente',  # Opção inválida
            'data_nascimento': 'data-invalida'  # Formato errado
        }
        
        response = self.client.post(
            reverse('editarAluno', kwargs={'cpf': '55'}),
            dados_invalidos
        )
        
        # Verifica resposta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TemplateEditarAluno.html")
        
        # Verifica erros no formulário
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('telefone', form.errors)
        self.assertIn('data_nascimento', form.errors)
        
        # Verifica se dados originais permanecem no banco
        aluno_banco = self.mongo._colecao.find_one({'cpf': '55'})
        self.assertEqual(aluno_banco['nome'], 'João Original')

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
            reverse('editarAluno', kwargs={'cpf': '55'}),
            {}
        )
        
        self.assertRedirects(response, reverse('paginaInicial'))

    def tearDown(self):
        # Limpar banco de dados
        self.mongo._colecao.delete_many({'cpf': '55'})

        self.mongo._colecao = self.mongo.mydb['personal']
        self.mongo._colecao.delete_many({'cpf':"12333678910"})
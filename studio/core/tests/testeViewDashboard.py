from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from core.views.View_Dashboard import DashboardView
from core.services.ConexaoMongo import ConexaoMongo
from unittest.mock import MagicMock


def adicionar_sessao_ao_request(request, sessao_dict):
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.update(sessao_dict)
    request.session.save()


class TestDashboardViewGET(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = DashboardView()

        # Mockar os métodos da repository para não depender do banco real
        self.view.alunoRepository.TodosAlunosPorStatus = MagicMock(return_value=[{"_id": "ativo", "qtd": 10}])
        self.view.alunoRepository.TodosAlunosPorPersonal = MagicMock(return_value=[{"id": "Personal X", "qtd": 5}])
        self.view.alunoRepository.TodosAlunosPorPlano = MagicMock(return_value=[{"id": "Mensal", "qtd": 7}])
        self.view.alunoRepository.tendenciaAssinatura = MagicMock(return_value={
            "novas_assinaturas": [],
            "renovacoes": [],
            "cancelamentos": []
        })
        self.view.alunoRepository.alunoPorIdade = MagicMock(return_value=[{"idade": 25, "qtd": 3}])

        # Criar personal admin real no banco (acesso = "adm")
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

        # Requisição GET simulada com client (sessão válida)
        self.response = self.client.get(reverse("dashboard"))

    def tearDown(self):
        # Limpar banco de dados após testes
        self.mongo._colecao.delete_many({'cpf': "12333678910"})

    def test_redireciona_sem_sessao(self):
        request = self.factory.get(reverse("dashboard"))
        adicionar_sessao_ao_request(request, {})

        response = self.view.get(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("paginaInicial"), response.url)

    def test_redireciona_se_nao_admin(self):
        request = self.factory.get(reverse("dashboard"))
        adicionar_sessao_ao_request(request, {
            "sessao": True,
            "tipo_usuario": "personal",
            "cpf": "00000000000"  # CPF que não existe no banco
        })

        response = self.view.get(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("paginaInicial"), response.url)

    def test_get_sucesso_com_admin(self):
        self.assertEqual(self.response.status_code, 200)

        context = self.response.context
        self.assertIn("balancoAlunos", context)
        self.assertIn("alunosPorPlano", context)
        self.assertIn("alunosPorPersonal", context)
        self.assertIn("alunosPorIdade", context)
        self.assertIn("tendenciaMeses", context)

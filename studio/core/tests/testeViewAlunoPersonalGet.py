from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from core.views.View_AlunoPersonal import AlunoPersonalView
from core.services.ConexaoMongo import ConexaoMongo


def adicionar_sessao_ao_request(request, sessao_dict):
    middleware = SessionMiddleware(lambda request: None)  # Passando get_response obrigatório
    middleware.process_request(request)
    request.session.update(sessao_dict)
    request.session.save()


class TestAlunoPersonalViewGET(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = AlunoPersonalView()
        self.personal = "Personal Teste"

        # Inserir alunos falsos no banco
        self.view.serviceM._colecao.delete_many({"cpf": {"$in": ["101", "102"]}})
        self.view.serviceM._colecao.insert_many([
            {"nome": "Ana", "cpf": "101", "personal": self.personal, "status": "ativo", "sessoes": []},
            {"nome": "Bruno", "cpf": "102", "personal": self.personal, "status": "ativo", "sessoes": []}
        ])

    def tearDown(self):
        self.view.serviceM._colecao.delete_many({"cpf": {"$in": ["101", "102"]}})

    def test_redireciona_se_sessao_invalida(self):
        request = self.factory.get(f"/alunos/{self.personal}")
        adicionar_sessao_ao_request(request, {})  # Sessão vazia

        response = self.view.get(request, self.personal)
        self.assertEqual(response.status_code, 302)  # Redireciona
        self.assertIn(reverse("paginaInicial"), response.url)



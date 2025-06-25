from django.test import TestCase, RequestFactory
from django.urls import reverse
from core.views.View_AlunoPersonal import AlunoPersonalView
from django.contrib.sessions.middleware import SessionMiddleware


def adicionar_sessao_ao_request(request, sessao_dict):
    middleware = SessionMiddleware(lambda request: None)  # Passando get_response obrigatório
    middleware.process_request(request)
    request.session.update(sessao_dict)
    request.session.save()


class TestAlunoPersonalViewPOST(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = AlunoPersonalView()
        self.personal = "Personal Teste"

    def test_post_ordem_ZA(self):
        request = self.factory.post(f"/alunos/{self.personal}", {"action": "Z-A"})
        adicionar_sessao_ao_request(request, {
            "sessao": True,
            "tipo_usuario": "personal",
            "admin": True,
        })

        response = self.view.post(request, self.personal)
        self.assertEqual(response.status_code, 302)
        self.assertIn("ordemAlunos=decrescente", response.url)

    def test_post_ordem_AZ(self):
        request = self.factory.post(f"/alunos/{self.personal}", {"action": "A-Z"})
        adicionar_sessao_ao_request(request, {
            "sessao": True,
            "tipo_usuario": "personal",
            "admin": True,
        })

        response = self.view.post(request, self.personal)
        self.assertEqual(response.status_code, 302)
        self.assertIn("ordemAlunos=crescente", response.url)

    def test_post_pesquisa(self):
        request = self.factory.post(f"/alunos/{self.personal}", {"action": "pesquisar", "pesquisaNome": "Carlos"})
        adicionar_sessao_ao_request(request, {
            "sessao": True,
            "tipo_usuario": "personal",
            "admin": True,
        })

        response = self.view.post(request, self.personal)
        self.assertEqual(response.status_code, 302)
        self.assertIn("pesquisaNome=Carlos", response.url)

    def test_post_acao_invalida_redireciona(self):
        request = self.factory.post(f"/alunos/{self.personal}", {"action": "invalido"})
        adicionar_sessao_ao_request(request, {
            "sessao": True,
            "tipo_usuario": "personal",
            "admin": True,
        })

        response = self.view.post(request, self.personal)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("paginaInicial"), response.url)

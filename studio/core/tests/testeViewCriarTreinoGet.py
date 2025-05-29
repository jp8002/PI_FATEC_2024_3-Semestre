from django.test import TestCase
from django.urls import  reverse

class TesteViewCriarTreinoGet(TestCase):
    def setUp(self):

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key


        self.resp = self.client.get(reverse("criarTreino"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateCriarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp,"<option")

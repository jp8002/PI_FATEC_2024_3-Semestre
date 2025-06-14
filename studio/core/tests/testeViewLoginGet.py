from django.test import TestCase
from django.urls import reverse


class TesteView_LoginGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('paginaLogin'))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code ,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateLogin.html")

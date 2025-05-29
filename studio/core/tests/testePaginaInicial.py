from django.test import TestCase
from django.urls import reverse


class TestePaginaInicial(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('paginaInicial'))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplatePaginaInicial.html")


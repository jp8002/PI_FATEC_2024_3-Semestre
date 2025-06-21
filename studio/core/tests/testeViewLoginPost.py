from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo


class TesteViewLoginPost(TestCase):
    def setUp(self):
        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['personal']
        self.id = self.mongo._colecao.insert_one({"nome" :"joao" ,"cpf" :"33" ,"senha" :"1234"})

        self.resp = self.client.post(reverse("paginaLogin") ,{ "cpf" :"33", "senha" :"1234"})

    def test_302_response(self):
        self.assertEqual(self.resp.status_code ,302)

    def test_template(self):
        self.assertRedirects(self.resp, reverse('paginaLogin'), status_code=302, target_status_code=302, fetch_redirect_response=True)

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':"33"})

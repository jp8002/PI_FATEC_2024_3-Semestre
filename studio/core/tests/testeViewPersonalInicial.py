from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo


class TesteViewPersonalInicial(TestCase):
    def setUp(self):

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['personal']
        self.id = self.mongo._colecao.insert_one({"nome" :"joao mock" ,"cpf" :"12345678910" ,"senha" :"1234"})

        session = self.client.session
        session["sessao" ] =True
        session["cpf" ] ="12345678910"

        session.save()

        self.client.cookies['sessionid'] = session.session_key

        self.resp = self.client.get(reverse("personalInicial"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code ,200)

    # def test_session_data(self):
    #     self.assertContains(self.resp,"joao mock")

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':"12345678910"})

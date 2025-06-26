
from django.test import TestCase
from django.urls import reverse

from core.entity.PersonalEntity import PersonalEntity
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo


class TestePaginaInicialComSessao(TestCase):

    def setUp(self):

        self.conn = ConexaoMongo()
        self.conn._colecao = self.conn.mydb['personal']

        self.personalEntity = PersonalEntity({"nome": "joao mock", "cpf": "1", "senha": "1234"})
        self.personalRepository = PersonalRepository(self.conn)

        self.id = self.personalRepository.criar(self.personalEntity)

        session = self.client.session
        session['sessao'] = True
        session['cpf'] = '1'
        session.save()

        self.client.cookies["sessionid"] = session.session_key
        self.resp = self.client.get(reverse('paginaInicial'))

    def test_302_response(self):

        self.assertEqual(self.resp.status_code, 302)

    def __del__(self):
        self.conn._colecao.delete_many({'cpf': "1"})
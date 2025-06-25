from django.test import TestCase
from django.urls import reverse
from core.services.Autenticar import Autenticar

from core.entity.PersonalEntity import PersonalEntity
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo

class TesteAutenticar(TestCase):

    def setUp(self):
        self.conn = ConexaoMongo()
        self.conn._colecao = self.conn.mydb['personal']
        self.session = self.client.session


# checarSessao
    def test_autenticar_sem_sessao(self):
        self.assertFalse (Autenticar.checarSessao(self.session))

    def test_autenticar_com_sessao(self):
        self.session['sessao'] = True
        self.session['cpf'] = '1'
        self.session.save()

        self.assertTrue(Autenticar.checarSessao(self.session))


# checarSessaoPersonal
    def test_autenticar_sem_sessao_personal(self):
        self.assertFalse(Autenticar.checarSessaoPersonal(self.session))

    def test_autenticar_com_sessao_personal(self):
        self.personalEntity = PersonalEntity({"nome": "joao mock", "cpf": "1", "senha": "1234"})
        self.personalRepository = PersonalRepository(self.conn)

        self.id = self.personalRepository.criar(self.personalEntity)

        self.session['sessao'] = True
        self.session['cpf'] = '1'
        self.session.save()

        self.assertTrue(Autenticar.checarSessaoPersonal(self.session))

    def __del__(self):
        self.conn._colecao.delete_many({'cpf': "1"})
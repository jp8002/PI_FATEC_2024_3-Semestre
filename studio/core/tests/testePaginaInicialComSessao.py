import ipdb
from django.test import TestCase
from django.urls import reverse

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.ConexaoMongo import ConexaoMongo


class TestePaginaInicialComSessao(TestCase):

    def setUp(self):

        self.conn = ConexaoMongo()
        self.conn._colecao = self.conn._mydb['aluno']

        self.alunoEntity = Aluno({"nome": "joao mock", "cpf": "123654789", "senha": "1234"})
        self.alunoRepository = AlunoRepository(self.conn)

        self.id = self.alunoRepository.criar(self.alunoEntity)

        session = self.client.session
        session['sessao'] = True
        session['cpf'] = '123654789'
        session.save()

        self.client.cookies["sessionid"] = session.session_key
        self.resp = self.client.get(reverse('paginaInicial'))

    def test_200_response(self):

        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):

        self.assertTemplateUsed(self.resp, "TemplatePaginaInicial.html")

    def __del__(self):
        self.conn._colecao.delete_many({'cpf': "123654789"})
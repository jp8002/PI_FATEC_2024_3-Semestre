from django.test import TestCase
from django.urls import reverse

from core.entity.PersonalEntity import PersonalEntity
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo

class TesteViewCadastrarPersonal(TestCase):
    def setUp(self):

        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['personal']

        self.personalRepository = PersonalRepository(self.mongo)

        session = self.client.session
        session["sessao" ] =True
        session["cpf" ] ="12333678910"

        session.save()

        self.client.cookies['sessionid'] = session.session_key

        self.resp = self.client.get(reverse("cadastrarPersonal"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code ,200)

    def test_criarNovoPersonal(self):
        NovoPersonal = {'nome':"joao mock", 'senha':"mock123", 'telefone':"999999999", 'email':"joao@mock.com", 'cpf':"12345678910"
                     , 'salario':"1000", 'acesso':"funcionario", 'cref':"999999-P/SP"}

        self.personalEntity = PersonalEntity(NovoPersonal)

        resultado = self.personalRepository.criar(self.personalEntity)

        self.assertTrue(resultado)

    def test_nao_adm(self):
        self.client.session.flush()

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["acesso"] = "funcionario"
        sessao['cpf'] = "12333678"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        NovoPersonal = {'nome':"joao mock", 'senha':"mock123", 'telefone':"999999999", 'email':"joao@mock.com", 'cpf':"12345678910"
                     , 'salario':"1000", 'acesso':"funcionario", 'cref':"999999-P/SP"}

        self.resp = self.client.post(reverse("cadastrarPersonal"), NovoPersonal)


    def __del__(self):
        self.mongo._colecao.delete_many({'cpf': "12345678910"})

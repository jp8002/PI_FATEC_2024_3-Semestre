from django.test import TestCase
from django.urls import reverse

from core.services.ConexaoMongo import ConexaoMongo

class TesteViewGerenciamentoAgendamentosPost(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12333678910"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key
        self.mongo = ConexaoMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']

        self.id = self.mongo._colecao.insert_one({"nome": "joao mock", "cpf": "12345678901", "senha": "1234", "sessoes":[]})

        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "12345678901", 'data': '2025-05-19T00:00','exercicios':['perna','coxa']})
        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "12345678901", 'data': '2025-06-19T00:00','exercicios':['perna','coxa']})
        self.resp = self.client.post(reverse("agendarTreino") ,{ 'cpf': "12345678901", 'data': '2025-07-19T00:00','exercicios':['perna','coxa']})

    def test_excluir(self):
        self.resp = self.client.post(
            reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}),
            {'acao': 'Excluir', 'dia': '2025-05-19T00:00'}
        )
        self.assertEqual(self.resp.status_code, 302)

    def test_salvar(self):
        self.resp = self.client.post(
            reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}),
            {'acao': 'Salvar', 'dia': '2025-05-19T00:00', 'exercicios': 'perna', 'idSessao': '0'}
        )
        self.assertEqual(self.resp.status_code, 302)

    def test_filtrar(self):
        self.resp = self.client.post(
            reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"}),
            {'acao': 'filtrar', 'dataEscolhida': '2025-05-19T00:00'}
        )

    def test_paginacao(self):
        # Acessa a URL sem parâmetro de página (deve retornar a primeira página)
        url = reverse("gerenciamentoAgendamentos", kwargs={"cpf": "12345678901"})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        sessoes = response.context['sessoes']
        # Verifica se há 3 sessões no total (3 páginas)
        self.assertEqual(sessoes.paginator.count, 3)
        # Verifica se está na página 1
        self.assertEqual(sessoes.number, 1)

        # Acessa a página 2
        response = self.client.get(url + '?page=2')
        sessoes = response.context['sessoes']
        self.assertEqual(sessoes.number, 1)
        self.assertEqual(len(sessoes.object_list), 3)

        # Acessa a página 3
        response = self.client.get(url + '?page=3')
        sessoes = response.context['sessoes']
        self.assertEqual(sessoes.number, 1)
        self.assertEqual(len(sessoes.object_list), 3)

        # Verifica comportamento com página inválida (deve retornar a última página)
        response = self.client.get(url + '?page=999')
        sessoes = response.context['sessoes']
        self.assertEqual(sessoes.number, sessoes.paginator.num_pages)

    def __del__(self):
        self.mongo._colecao.delete_many({'cpf':'12345678901'})
    
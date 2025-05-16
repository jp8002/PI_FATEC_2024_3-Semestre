from django.test import TestCase
from django.urls import reverse as r
from core.services import ServiceMongo
from bson.objectid  import ObjectId
import pymongo
import ipdb

# Create your tests here.

class testePaginaInicial(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('paginaInicial'))
        
    def test_200_response(self):
         self.assertEqual(self.resp.status_code,200)
    
    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplatePaginaInicial.html")
        

class testePaginaInicialComSessao(TestCase):
    def setUp(self):
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"123654789","senha":"1234"})
        
        
        session = self.client.session
        session['sessao'] = True
        session['cpf'] = '123654789'
        session.save()
        
        self.client.cookies["sessionid"] = session.session_key
        self.resp = self.client.get(r('paginaInicial'))
        
        
    def test_200_response(self):
         self.assertEqual(self.resp.status_code,200)
    
    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplatePaginaInicial.html")
        
    def test_template_session(self):
        self.assertContains(self.resp, "joao mock")
    
    def __del__ (self):
        self.mongo.consultarCpf("123654789")
        

class testeView_LoginGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('paginaLogin'))
        
    def test_200_response(self):
         self.assertEqual(self.resp.status_code,200)
    
    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateLogin.html")
        

class testeView_LoginPost(TestCase):
    def setUp(self):
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.id = self.mongo._colecao.insert_one({"nome":"joao","cpf":"123654789","senha":"1234"})
        
        self.resp = self.client.post(r("paginaLogin"),{ "cpf":"123654789", "senha":"1234", "tipo_usuario":"aluno"})
    
    def test_302_response(self):
         self.assertEqual(self.resp.status_code,302)
        
    def test_template(self):
        self.assertRedirects(self.resp, r('paginaLogin'), status_code=302, target_status_code=302, fetch_redirect_response=True)
        
    def __del__(self):
        self.mongo.deletarByCpf("123654789")


class testeView_AlunoInicial(TestCase):
    def setUp(self):
        
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"123654789","senha":"1234"})
        
        session = self.client.session
        session["sessao"]=True
        session["cpf"] = "123654789"
        
        session.save()
        
        self.client.cookies['sessionid'] = session.session_key
        
        self.resp = self.client.get(r("alunoInicial"))
        
    
    def test_200_response(self):
         self.assertEqual(self.resp.status_code,200)
         
    # def test_session_data(self):
    #     self.assertContains(self.resp,"joao mock")
        
    
    def __del__(self):
        self.mongo.deletarByCpf("123654789")
        
class testeView_PersonalInicial(TestCase):
    def setUp(self):

        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['personal']
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"12345678910","senha":"1234"})

        session = self.client.session
        session["sessao"]=True
        session["cpf"]="12345678910"

        session.save()

        self.client.cookies['sessionid'] = session.session_key

        self.resp = self.client.get(r("personalInicial"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    # def test_session_data(self):
    #     self.assertContains(self.resp,"joao mock")

    def __del__(self):
        self.mongo.deletarByCpf("12345678910")
    
class testeView_CadastrarPersonal(TestCase):
    def setUp(self):

        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['personal']

        session = self.client.session
        session["sessao"]=True
        session["cpf"]="12345678910"

        session.save()

        self.client.cookies['sessionid'] = session.session_key

        self.resp = self.client.get(r("cadastrarPersonal"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_criarNovoPersonal(self):
        resultado = self.mongo.criarNovoPersonal("joao mock", "mock123", "999999999", "joao@mock.com","12345678910","1000","funcionario","999999-P/SP")
        self.assertTrue(resultado)
        
    def __del__(self):
        self.mongo.deletarByCpf("12345678910")


class testeView_CadastrarAluno_Get(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"]=True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.resp = self.client.get(r("cadastrarAluno"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateCadastrarAluno.html")


class testeView_CadastrarAluno_Post(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"]=True
        sessao['tipo_usuario'] = "personal"
        sessao['cpf'] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key

        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']

        aluno = {"nome": "joao mock", "data_nascimento":"2019-05-20" , "cpf": "123456789", "telefone": "123456"}

        self.resp = self.client.post(r("cadastrarAluno"), aluno)

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_post(self):
        x = self.mongo.consultarCpf("123456789")
        self.assertEqual(x.get("nome", "Não foi possível encontrar"),"joao mock")


    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateCadastrarAluno.html")
        
    def __del__(self):
        self.mongo.deletarByCpf("123456789")


class testeView_AgendarTreino_Get(TestCase):
    def setUp(self):

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key


        self.resp = self.client.get(r("agendarTreino"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateAgendarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp,"<option")

class testeView_AgendarTreino_Post(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key
        
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"123456789","senha":"1234"})

        self.resp = self.client.post(r("agendarTreino"),{ 'cpf': '123456789', 'dia': '2025-05-19T00:00'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateAgendarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo.deletarByCpf("123456789")

class testeView_DeletarAgendamento_Get(TestCase):
    def setUp(self):

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key


        self.resp = self.client.get(r("deletarAgendamento"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateDeletarAgendamento.html")

    def test_combobox(self):
        self.assertContains(self.resp,"<option")

class testeView_DeletarAgendamento_Post(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key
        
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.mongo._colecao.update_one({"cpf":"123456789"},{"$push": {"sessoes": "2025-05-19T00:00"}})
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"123456789","senha":"1234"})

        self.resp = self.client.post(r("deletarAgendamento"),{ 'cpf': '123456789', 'dia': '2025-05-19T00:00'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateDeletarAgendamento.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo.deletarByCpf("123456789")

class testeView_CriarTreino_Get(TestCase):
    def setUp(self):

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key


        self.resp = self.client.get(r("criarTreino"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateCriarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp,"<option")

class testeView_CriarTreino_Post(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key
        
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']

        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"123456789","senha":"1234"})

        self.resp = self.client.post(r("criarTreino"),{ 'cpf': '123456789', 'treino': 'Remada'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateCriarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo.deletarByCpf("123456789")

class testeView_DeletarTreino_Get(TestCase):
    def setUp(self):

        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key


        self.resp = self.client.get(r("deletarTreino"))

    def test_200_response(self):
        self.assertEqual(self.resp.status_code,200)

    def test_template(self):
        self.assertTemplateUsed(self.resp,"TemplateDeletarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp,"<option")

class testeView_DeletarTreino_Post(TestCase):
    def setUp(self):
        sessao = self.client.session
        sessao["sessao"] = True
        sessao['tipo_usuario'] = "personal"
        sessao["cpf"] = "12345678901"
        sessao.save()

        self.client.cookies['sessionid'] = sessao.session_key
        
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['aluno']
        self.mongo._colecao.update_one({"cpf":"123456789"},{"$push": {"treinos": "Remada"}})
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","cpf":"123456789","senha":"1234"})

        self.resp = self.client.post(r("deletarTreino"),{ 'cpf': '123456789', 'treino': 'Remada'})

    def test_200_response(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "TemplateDeletarTreino.html")

    def test_combobox(self):
        self.assertContains(self.resp, "<option")

    def __del__(self):
        self.mongo.deletarByCpf("123456789")


class testeServiceMongo(TestCase):
    def setUp(self):
        self.mongo = ServiceMongo('localhost', '27017', "mock")
        self.mongo._colecao = self.mongo._mydb['mockcol']
        self.id = self.mongo._colecao.insert_one({"nome": "joao", "cpf": "123654789"})

        self.mongo._colecao.insert_one({
            "status": "ativo",
            "data_assinatura": "2024-03-01T08:00:00"
        })
        self.mongo._colecao.insert_one({
            "status": "inativo",
            "data_assinatura": "2024-03-02T09:00:00"
        })

    def test_ChecarAluno(self):
        resp = self.mongo.ChecarAluno(self.id.inserted_id)
        # ipdb.set_trace()
        self.assertEqual(resp, True)

    def test_consultar(self):
        resp = self.mongo.consultar(self.id.inserted_id)
        nomeBanco = resp.get("nome", "Essa chave não existe")

        self.assertEqual(nomeBanco, "joao")

    def test_consultar_datas_agendadas(self):
        resp = self.mongo.consultar_datas_agendadas()
        self.assertIn("01/03/2024", resp)
        self.assertNotIn("02/03/2024", resp)

    def test_consultarCpf(self):
        resp = self.mongo.consultarCpf("123654789")
        self.assertEqual(resp.get("nome", "Não foi encontrado"), "joao")

    def test_deletarByCpf(self):
        resp = self.mongo.deletarByCpf("123654789")
        self.assertEqual(resp, True)

    def test_criarNovoPersonal(self):
        resp = self.mongo.criarNovoPersonal("Otavio", "otavio123", "999999999", "otavio@gmail.com", "12345678910",
                                            "1500","funcionario","999999-P/SP")
        self.assertTrue(resp)

    def test_criarNovoAluno(self):
        resp = self.mongo.CriarNovoAluno(
            {"nome": "joao mock", "data_nascimento": "2019-05-20", "cpf": "123654789", "status": "ativo","telefone": "123424564646"})
        self.assertTrue(resp)

    def test_listaAlunos(self):
        resp = self.mongo.listarAlunos()
        #ipdb.set_trace()
        self.assertTrue(resp)

    def test_agendar(self):
        resp = self.mongo.agendar({"cpf":"123654789","dia":"2025-05-06T20:06"})
        self.assertTrue(resp)

    def test_deletarAgendamento(self):
        self.mongo.agendar({"cpf":"123654789","dia":"2025-05-06T20:06"})
        resp = self.mongo.deletarAgendamento({"cpf":"123654789","dia":"2025-05-06T20:06"})
        self.assertTrue(resp)

    def test_CriarTreinoAluno(self):
        resp = self.mongo.CriarTreinoAluno("123654789","Crucifixo")
        self.assertTrue(resp)

    def test_deletarTreinoAluno(self):
        self.mongo.CriarTreinoAluno("123654789", "Crucifixo")
        resp = self.mongo.deletarTreinoAluno("123654789","Crucifixo")
        self.assertTrue(resp)

    def test_listaPersonals(self):
        resp = self.mongo.listarPersonals()

        self.assertTrue(resp)

    def test_atualizarPersonal(self):
        cpf="12345678910"
        self.mongo.criarNovoPersonal("mock peres", "mock123","999999999","peres@mock.com",cpf,"1500","funcionario","999999-P/SP")

        novo_telefone="912345678"
        novo_email="peres@mock.com"
        novo_salario="1600"
        novo_acesso="admin"

        resp = self.mongo.atualizarPersonal(cpf,novo_telefone,novo_email,novo_salario,novo_acesso)
        self.assertTrue(resp)

        registro_atualizado = self.mongo._colecao.find_one({"cpf": cpf})
        self.assertEqual(registro_atualizado["telefone"], novo_telefone)
        self.assertEqual(registro_atualizado["email"], novo_email)
        self.assertEqual(registro_atualizado["salario"], float(novo_salario))
        self.assertEqual(registro_atualizado["acesso"], novo_acesso)
        self.assertEqual(registro_atualizado["nome"], "mock peres") 
        self.assertEqual(registro_atualizado["cref"], "999999-P/SP")
    
    def test_editarAluno(self):
        resp = self.mongo.editarAluno({"nome": "joao fake", "data_nascimento": "2019-10-27", "status":"ativo" ,"cpf":"123654789" , "telefone": "963258741"})
        self.assertTrue(resp)

    def test_deletarAluno(self):
        resp = self.mongo.deletarAluno("123654789")
        self.assertEqual(resp, True)

    def test_listarAlunosPorStatus(self):
        resp= self.mongo.listarAlunosPorStatus("ativo")
        self.assertTrue(resp)

    def __del__(self):
        self.mongo._colecao.drop()

            
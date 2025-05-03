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
        self.mongo._colecao = self.mongo._mydb['clientes']
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","rg":"123654789","senha":"1234"})
        
        
        session = self.client.session
        session['sessao'] = [True]
        session['rg'] = '123654789'
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
        self.mongo.consultarRg("123654789")
    
    
class testeServiceMongo(TestCase):
    def setUp(self):
        
        self.mongo = ServiceMongo('localhost','27017',"mock")
        self.mongo._colecao = self.mongo._mydb['mockcol']
        self.id = self.mongo._colecao.insert_one({"nome":"joao", "rg":"123654789"})

        self.mongo._colecao.insert_one({
            "status": "ativo",
            "data_assinatura": "2024-03-01T08:00:00"
        })
        self.mongo._colecao.insert_one({
            "status": "inativo",
            "data_assinatura": "2024-03-02T09:00:00"
        })

    def test_Checar_cliente(self):
            resp = self.mongo.Checar_cliente(self.id.inserted_id)
            #ipdb.set_trace()
            self.assertEqual(resp, True)
    
    def test_consultar(self):
        resp = self.mongo.consultar(self.id.inserted_id)
        nomeBanco = resp.get("nome","Essa chave não existe")
        
        self.assertEqual(nomeBanco, "joao")

    def test_consultar_datas_agendadas(self):
        resp = self.mongo.consultar_datas_agendadas()
        self.assertIn("01/03/2024", resp)
        self.assertNotIn("02/03/2024", resp)
    
    def test_consultarRg(self):
        resp = self.mongo.consultarRg("123654789")
        self.assertEqual(resp.get("nome","Não foi encontrado"), "joao")
    
    def deletarPersonalByCpf(self):
        resp = self.mongo.deletarPersonalByCpf("123654789")
        self.assertEqual(resp, True)
    

    def __del__(self):
        self.mongo._colecao.drop()
        

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
        self.mongo._colecao = self.mongo._mydb['clientes']
        self.id = self.mongo._colecao.insert_one({"nome":"joao","rg":"123654789","senha":"1234"})
        
        self.resp = self.client.post(r("paginaLogin"),{ "rg":"123654789", "senha":"1234"})
    
    def test_302_response(self):
         self.assertEqual(self.resp.status_code,302)
        
    def test_template(self):
        self.assertRedirects(self.resp, r('paginaInicial'), status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def __del__(self):
        self.mongo.deletarPersonalByCpf("123654789")


class testeView_AlunoInicial(TestCase):
    def setUp(self):
        
        self.mongo = ServiceMongo()
        self.mongo._colecao = self.mongo._mydb['clientes']
        self.id = self.mongo._colecao.insert_one({"nome":"joao mock","rg":"123654789","senha":"1234"})
        
        session = self.client.session
        session["sessao"]=True,
        session["rg"] = "123654789"
        
        session.save()
        
        self.client.cookies['sessionid'] = session.session_key
        
        self.resp = self.client.get(r("alunoInicial"))
        
    
    def test_200_response(self):
         self.assertEqual(self.resp.status_code,200)
         
    def test_session_data(self):
        self.assertContains(self.resp,"joao mock")
        
    
    def __del__(self):
        self.mongo.deletarPersonalByCpf(123654789)
        

    
    
        
            
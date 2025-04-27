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
        

# class testePaginaInicialComSessao(TestCase):
#     def setUp(self):
        
#         session = self.client.session
#         session['Sessao'] = [True]
#         session['ClienteID'] = '67fee5d803975827916334c5'
#         session.save()
#         self.resp = self.client.get(r('paginaInicial'))
        
        
#     def test_200_response(self):
#          self.assertEqual(self.resp.status_code,200)
    
#     def test_template(self):
#         self.assertTemplateUsed(self.resp, "TemplatePaginaInicial.html")
        
#     def test_template_session(self):
#         self.assertContains(self.resp, "Ana Silva")
    
class testeServiceMongo(TestCase):
    def setUp(self):
        
        self.mongo = ServiceMongo('localhost','27017',"mock")
        self.mongo._colecao = self.mongo._mydb['mockcol']
        self.id = self.mongo._colecao.insert_one({"nome":"joao"})

    def test_Checar_cliente(self):
        resp = self.mongo.Checar_cliente(self.id.inserted_id)
        #ipdb.set_trace()
        self.assertEqual(resp, True)
    
    def test_consultar(self):
        resp = self.mongo.consultar(self.id.inserted_id)
        nomeBanco = resp.get("nome","Essa chave não existe")
        
        self.assertEqual(nomeBanco, "joao")
        
    def __del__(self):
        self.mongo._colecao.drop()
        
        
    
        
            
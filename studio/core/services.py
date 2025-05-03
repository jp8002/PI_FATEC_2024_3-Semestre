from queue import Full
import pymongo
from bson.objectid  import ObjectId
from django.shortcuts import render, redirect #checar com o prfessor
from datetime import datetime
import ipdb

class Autenticar:
    # def AuthSession(cookies):
    #     if not request.session.get("ClienteID", False):
    #         return False
            
    #     ClienteID = request.session.get("ClienteID", False)
        
    #     if ServiceMongo.Checar_cliente(ClienteID):
    #         request.session["Sessao"] = TRUE
    
    def AuthUsuario(usuario):
        if usuario.get("tipo_usuario" == "cliente"):
            if not ("rg" and "senha" in usuario):
                raise Exception("O dict post não possui todos as chaves")
                return False
            
            if not usuario.get("rg") or not usuario.get("senha"):
                raise Exception("Os campos não foram completamente preenchidos")
                return False
        
       
            MongoClient = ServiceMongo()
            MongoClient._colecao = MongoClient._mydb["clientes"]
        
            query = MongoClient.consultarRg(usuario.get("rg"))
            
            if not (query.get("senha") == usuario.get('senha')):
                raise Exception("Senha errada")
                return False
            
            return True
        
        else:
            if usuario.get("tipo_usuario" == "personal"):
                cpf = usuario.get("cpf")

                if not (cpf and "senha" in usuario):
                    raise Exception("O dict post não possui todas as chaves")
                    return False
                
                if not usuario.get(cpf) or not usuario.get("senha"):
                    raise Exception("Os campos não foram compleatamente preenchidos")
                    return False
                
                MongoClient = ServiceMongo()
                MongoClient._colecao = MongoClient._mydb["personals"]

                query = MongoClient.consultarCpf(usuario.get(cpf))

                if not (query.get("senha") == usuario.get('senha')):
                    raise Exception("Senha errada")
                    return False
                
            return True
        
    def checarSessao(sessao):
        if (sessao.get('sessao',False) and sessao.get("rg",False)) or (sessao.get('sessao',False) and sessao.get("cpf", False)):
            return True
        
        return False
    
    def checarSessaoCliente(sessao):
        if sessao.get('sessao',False) and sessao.get("rg", False):
            return True

        return False
        
    def checarSessaoPersonal(sessao):
        if sessao.get('sessao',False) and sessao.get("cpf", False):
            return True

        return False    
        
        
            

class ServiceMongo:
    

    def __init__(self, host="localhost", port = "27017", db = "studio"):
        try:
            self._client = pymongo.MongoClient('mongodb://' + host + ':' + port + '/')
            self._mydb = self._client[db]
            self._colecao = None
        except Exception as e:
            raise Exception("Erro ao conectar o banco de dados: " + str(e))
            return False
        
        
    def Checar_cliente(self,id):
        
        cliente = self._colecao.find_one(ObjectId(id))
        
        if len(list(cliente)) == 0:
            return False
    
        return True    
    
    def consultarRg(self,rg):
        
        #ipdb.set_trace()
        
        cliente = self._colecao.find_one({"rg":rg})
        
        if len(list(cliente)) == 0:
            return False
    
        return cliente
    
        
    def consultar(self,id):
        
        cliente = self._colecao.find_one(ObjectId(id))
        
        if  len(list(cliente)) == 0:
            return False
    
        return cliente
    
    def consultar_datas_agendadas(self): # O MÉTODO ATUALMENTE RETORNA TODAS AS DATAS (BASEADAS NAS ASSINATURAS ATIVAS) NO FORMATO DD/MM/AAAA
        datas_agendadas = []
        
        query = {"status":"ativo"}
        for cadastro in self._colecao.find(query):
            if "data_assinatura" in cadastro:
                data_str = cadastro["data_assinatura"]
                data_datetime = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
                data = data_datetime.strftime("%d/%m/%Y")
                datas_agendadas.append(data)

        return datas_agendadas
    
    def deletarPersonalByCpf(self, cpf):
        try:
            self._colecao.delete_many({"cpf":cpf})
            return True
        except Exception as e:
            raise Exception("Não foi possivel deletar o registro ", e)
            return False
        
    def criarNovoPersonal(self, nome, senha, telefone, email, cpf, salario):
        try:
            self._colecao.insert_one({
                "nome": nome,
                "senha": senha,
                "telefone": telefone,
                "email": email,
                "cpf": cpf,
                "salario": salario
            })
            return True
        except Exception as e:
            raise Exception("Erro na criação do registro ", e)
            return False
        
    def consultarCpf(self, rg):
        cpf = rg
        personal = self._colecao.find_one({"cpf":cpf})
        
        if len(list(personal)) == 0:
            return False
    
        return personal

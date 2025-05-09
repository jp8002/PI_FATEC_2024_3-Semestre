import logging
from queue import Full
import pymongo
from bson.objectid  import ObjectId
from django.shortcuts import render, redirect #checar com o prfessor
from datetime import datetime
import ipdb

logging.basicConfig(
    level=logging.ERROR,
    format='%(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
)

class Autenticar:
    def AuthUsuario(usuario):

        cpf = usuario.get("cpf", None)
        senha = usuario.get("senha", None)
        tipo_usuario = usuario.get("tipo_usuario", None)

        if not cpf or not senha or not tipo_usuario:
            raise Exception("Os campos não foram completamente preenchidos")
            #return False

        MongoClient = ServiceMongo()
        MongoClient._colecao = MongoClient._mydb[tipo_usuario]

        query = MongoClient.consultarCpf(cpf)
        if not (query.get("senha") == senha):
            raise Exception("Senha errada")
            #return False
                
        return True
        
    def checarSessao(sessao):
        if (not sessao.get('sessao',False) or not  sessao.get("cpf",False)):
            return False

        if sessao.get("sessao",False) != True:
            return False
        
        return True
    
    def checarSessaoAluno(sessao):
        if not sessao.get("tipo_usuario", False) == "aluno":
            return False

        MongoClient = ServiceMongo()
        MongoClient._colecao = MongoClient._mydb["aluno"]
        if not MongoClient.consultarCpf(sessao.get("cpf",False)):
            return False

        return True
        
    def checarSessaoPersonal(sessao):
        if not sessao.get("tipo_usuario", False) == "personal":
            return False

        MongoClient = ServiceMongo()
        MongoClient._colecao = MongoClient._mydb["personal"]
        if not MongoClient.consultarCpf(sessao.get("cpf", False)):
            return False

        return True

class ServiceMongo:
    

    def __init__(self, host="localhost", port = "27017", db = "studio"):
        try:
            self._client = pymongo.MongoClient('mongodb://' + host + ':' + port + '/')
            self._mydb = self._client[db]
            self._colecao = None
        except Exception as e:
            raise Exception("Erro ao conectar o banco de dados: " + str(e))
            #return False
        
        
    def ChecarAluno(self,id):
        
        aluno = self._colecao.find_one(ObjectId(id))
        
        if len(list(aluno)) == 0:
            raise Exception("Esse aluno não existe")
    
        return True    
    
    def consultarCpf(self,cpf):
        
        #ipdb.set_trace()
        
        query = self._colecao.find_one({"cpf":cpf})
        
        try:
            list(query)

        except Exception as e:
            logging.error("Esse cpf não existe (" + str(e) + ")")
            return False

        return query
    
        
    def consultar(self,id):
        
        query = self._colecao.find_one(ObjectId(id))
        
        if  len(list(query)) == 0:
            raise Exception("Esse id não existe")
    
        return query
    
    def consultar_datas_agendadas(self): # O METODO ATUALMENTE RETORNA TODAS AS DATAS (BASEADAS NAS ASSINATURAS ATIVAS) NO FORMATO DD/MM/AAAA
        datas_agendadas = []
        
        query = {"status":"ativo"}
        for cadastro in self._colecao.find(query):
            if "data_assinatura" in cadastro:
                data_str = cadastro["data_assinatura"]
                data_datetime = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
                data = data_datetime.strftime("%d/%m/%Y")
                datas_agendadas.append(data)

        return datas_agendadas
    
    def deletarByCpf(self, cpf):
        try:
            self._colecao.delete_many({"cpf":cpf})
            return True
        except Exception as e:
            raise Exception("Não foi possivel deletar o registro ", e)
            #return False
        
    def criarNovoPersonal(self, nome, senha, telefone, email, cpf, salario):
        try:
            salario = float(salario)
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
            #return False

    def CriarNovoAluno(self, DadosAluno):
        try:
            nome = DadosAluno["nome"]
            data_nascimento = DadosAluno["data_nascimento"]
            cpf = DadosAluno["cpf"]
            telefone = DadosAluno["telefone"]

            query = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "telefone": telefone}

            self._colecao.insert_one(query)
            return True
        except Exception as e:
            raise Exception("Não foi possivel criar o registro ", e)


    def listarAlunos(self):
        try:
            query = list(self._colecao.find())

        except Exception as e:
            logging.error("Erro ao consultar o registro ", e)
            return False

        return query

    def agendar(self,Agendamento):
        cpf = Agendamento["cpf"]
        dia = Agendamento["dia"]

        if (self.consultarCpf(cpf) == False):
            raise Exception("Esse cpf não existe")

        try:
            dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")
        except Exception as e:
            logging.error("Erro ao converter o dia ", e)
            return False

        self._colecao.update_one({"cpf":cpf},{"$push":{"sessoes":dia}})
        return True

    def deletarAgendamento(self,Agendamento):
        cpf = Agendamento["cpf"]
        dia = Agendamento["dia"]

        if (self.consultarCpf(cpf) == False):
            raise Exception("Esse cpf não existe")

        try:
            dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")
        except Exception as e:
            logging.error("Erro ao converter o dia ", e)
            return False

        self._colecao.update_one({"cpf":cpf},{"$pull":{"sessoes":dia}})
        return True

    def CriarTreinoAluno(self, cpfAluno,treino):
        try:
            treinoAdicao = self._colecao.update_one(
                {"cpf": cpfAluno},
                {"$push": {"treinos":treino}}
            )

            if treinoAdicao.modified_count == 0:
                raise Exception("Verifique se o CPF está correto.")
                return False
            
            return True

        except Exception as e:
            logging.error("Erro ao adicionar treino: (" + str(e) + ")")

    def deletarTreinoAluno(self, cpfAluno, treino):
        try:
            treinoRemocao = self._colecao.update_one(
                {"cpf":cpfAluno},
                {"$pull": {"treinos":treino}}
            )

            if treinoRemocao.modified_count == 0:
                raise Exception(f"Treino '{treino}' não encontrado para o CPF {cpfAluno}")
                return False
        except Exception as e:
            logging.error("Erro ao deletar treino: (" + str(e) + ")")
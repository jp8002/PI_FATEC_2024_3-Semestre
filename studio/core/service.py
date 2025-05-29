import logging
import pymongo
from bson.objectid  import ObjectId
from datetime import datetime

from core.repositories.AlunoRepository import AlunoRepository
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo

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

        MongoClient = ConexaoMongo()
        MongoClient._colecao = MongoClient._mydb[tipo_usuario]

        #esdras
        if tipo_usuario == "aluno":
            alunoRepository = AlunoRepository(MongoClient)
            query = alunoRepository.consultarCpf(cpf)
        else:
            personalRepository = PersonalRepository(MongoClient)
            query = personalRepository.consultarCpf(cpf)

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

        MongoClient = ConexaoMongo()
        MongoClient._colecao = MongoClient._mydb["aluno"]

        alunoRepository = AlunoRepository(MongoClient)

        if not alunoRepository.consultarCpf(sessao.get("cpf",False)):
            return False

        return True
        
    def checarSessaoPersonal(sessao):
        if not sessao.get("tipo_usuario", False) == "personal":
            return False

        MongoClient = ConexaoMongo()
        MongoClient._colecao = MongoClient._mydb["personal"]

        personalRepository = PersonalRepository(MongoClient)

        if not personalRepository.consultarCpf(sessao.get("cpf", False)):
            return False

        return True



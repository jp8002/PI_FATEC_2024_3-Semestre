import logging

from core.repositories.AlunoRepository import AlunoRepository
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo

class Autenticar():

    def checarSessao(sessao):
        if (not sessao.get('sessao',False) or not  sessao.get("cpf",False)):
            return False

        if sessao.get("sessao",False) != True:
            return False
        
        return True
        
    def checarSessaoPersonal(sessao):
        MongoClient = ConexaoMongo()
        MongoClient._colecao = MongoClient._mydb["personal"]

        personalRepository = PersonalRepository(MongoClient)

        if not personalRepository.consultarCpf(sessao.get("cpf", False)):
            return False

        return True



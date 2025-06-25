
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
        MongoClient._colecao = MongoClient.mydb["personal"]

        personalRepository = PersonalRepository(MongoClient)

        if not personalRepository.consultarCpf(sessao.get("cpf", False)):
            return False

        return True
    
    def checarAdmin(sessao):
        MongoClient = ConexaoMongo()
        MongoClient._colecao = MongoClient.mydb["personal"]

        personalRepository = PersonalRepository(MongoClient)

        personal = personalRepository.consultarCpf(sessao.get("cpf", False))

        if not personal:
            return False
        
        if personal.get("acesso", "") != "adm":
            return False
        
        return True



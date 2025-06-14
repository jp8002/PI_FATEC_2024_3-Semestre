import logging

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

        if not cpf or not senha:
            raise Exception("Os campos não foram completamente preenchidos")

        MongoClient = ConexaoMongo()
        MongoClient._colecao = MongoClient._mydb['personal']

        #esdras
        
        personalRepository = PersonalRepository(MongoClient)
        query = personalRepository.consultarCpf(cpf)

        if not (query.get("senha") == senha):
            raise Exception("Senha errada")
                
        return True
        
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



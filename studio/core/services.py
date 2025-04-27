import pymongo
from bson.objectid  import ObjectId

class Autenticar:
    def AuthSession(cookies):
        if not request.session.get("ClienteID", False):
            return False
            
        ClienteID = request.session.get("ClienteID", False)
        
        if ServiceMongo.Checar_cliente(ClienteID):
            request.session["Sessao"] = TRUE

class ServiceMongo:
    def __init__(self, host="localhost", port = "27017", db = "studio"):
        try:
            self._client = pymongo.MongoClient('mongodb://' + host + ':' + port + '/')
            self._mydb = self._client[db]
        except Exception as e:
            print("Erro ao conectar o banco de dados: " + str(e))
        
    def Checar_cliente(self,id):
        
        cliente = self._colecao.find_one(ObjectId(id))
        
        if len(list(cliente)) == 0:
            return False
    
        return True
        
    def consultar(self,id):
        
        cliente = self._colecao.find_one(ObjectId(id))
        
        if  len(list(cliente)) == 0:
            return False
    
        return cliente
    

        
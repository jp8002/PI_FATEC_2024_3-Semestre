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
    def Checar_cliente(id):
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017')
            mydb = client["studio"]
            colecao = mydb["clientes"]
            
            cliente = colecao.find_one(ObjectId(id))
        
        except:
            print("Erro ao utilizar o banco de dados")
            return False
        
        if len(list(cliente)) == 0:
            return False
    
        return True
        
    def consultar(id):
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017')
            mydb = client["studio"]
            colecao = mydb["clientes"]
            
            cliente = colecao.find_one(ObjectId(id))
        
        except:
            print("Erro ao utilizar o banco de dados")
            return False
        
        if  len(list(cliente)) == 0:
            return False
    
        return cliente
    

        
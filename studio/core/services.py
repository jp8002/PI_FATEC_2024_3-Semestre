import pymongo
from bson.objectid  import ObjectId

class ServiceMongo:
    def consultar(self, id):
        client = pymongo.MongoClient('mongodb://localhost:27017')
        mydb = client["studio"]
        colecao = mydb["clientes"]
        
        x = colecao.find_one(ObjectId(id))
        
        return x
        
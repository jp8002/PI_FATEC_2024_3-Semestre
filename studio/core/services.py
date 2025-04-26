import pymongo
from bson.objectid  import ObjectId
from datetime import datetime

class ServiceMongo:
    def consultar(self, id):
        client = pymongo.MongoClient('mongodb://localhost:27017')
        mydb = client["studio"]
        colecao = mydb["clientes"]
        
        x = colecao.find_one(ObjectId(id))
        
        return x

    def consultar_datas_agendadas(self): # O MÉTODO ATUALMENTE RETORNA TODAS AS DATAS (BASEADAS NAS ASSINATURAS ATIVAS) NO FORMATO DD/MM/AAAA
        client = pymongo.MongoClient('mongodb://localhost:27017')
        mydb = client["studio"]
        colecao = mydb["clientes"]
        
        datas_agendadas = []
        
        query = {"status":"ativo"}
        for cadastro in colecao.find(query):
            if "data_assinatura" in cadastro:
                data_str = cadastro["data_assinatura"]
                data_datetime = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
                data = data_datetime.strftime("%d/%m/%Y")
                datas_agendadas.append(data)
        
        return datas_agendadas
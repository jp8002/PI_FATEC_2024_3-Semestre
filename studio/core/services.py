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
    

        
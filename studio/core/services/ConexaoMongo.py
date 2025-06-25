import pymongo

class ConexaoMongo:

    def __init__(self, host="localhost", port = "27017", db = "studio"):
        try:
            self.client = pymongo.MongoClient('mongodb://' + host + ':' + port + '/')
            self.mydb = self.client[db]
        except Exception as e:
            raise Exception("Erro ao conectar o banco de dados: " + str(e))
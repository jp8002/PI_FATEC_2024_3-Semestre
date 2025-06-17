import pymongo

class ConexaoMongo:

    def __init__(self, host="localhost", port = "27017", db = "studio"):
        try:
            self._client = pymongo.MongoClient('mongodb://' + host + ':' + port + '/')
            self._mydb = self._client[db]
        except Exception as e:
            raise Exception("Erro ao conectar o banco de dados: " + str(e))
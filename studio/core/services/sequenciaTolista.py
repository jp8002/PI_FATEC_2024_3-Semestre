

class sequenciaTolista():
    @staticmethod
    def strTolista(lista):
        lista = lista.replace('\n','')
        lista = lista.replace('\r','')
        return lista.split(";")
from abc import ABCMeta, abstractmethod

class InterfaceRepository(metaclass=ABCMeta):

    @abstractmethod
    def criar(self, entity):
        pass

    @abstractmethod
    def consultarCpf(self, cpf):
        pass

    @abstractmethod
    def consultarId(self, id):
        pass

    @abstractmethod
    def deletarById(self, entity):
        pass

    @abstractmethod
    def listarTodos(self):
        pass

    @abstractmethod
    def atualizar(self, entity):
        pass



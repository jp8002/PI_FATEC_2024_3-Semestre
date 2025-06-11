import logging
from datetime import datetime

import ipdb
from bson import ObjectId

from core.entity.AlunoEntity import Aluno
from core.interfaces.InterfaceRepository import InterfaceRepository
from core.repositories.AlunoRepository import AlunoRepository


class PersonalRepository(InterfaceRepository):
    def __init__(self, mongo):
        self.mongo = mongo

    def criar(self, entity):
        
        if self.consultarCpf(entity.cpf):
            raise Exception('Esse personal já está cadastrado')
            
        try:
            dados = entity.__dict__
            self.mongo._colecao.insert_one(dados)
            return True

        except Exception as e:
            raise Exception("Não foi possivel criar o registro ", e)

    def consultarCpf(self, cpf):

        try:
            query = self.mongo._colecao.find_one({"cpf": cpf})

        except Exception as e:
            raise Exception("Erro ao consultar cpf (" + str(e) + ")")

        return query

    def deletarById(self, entity):
        try:
            self.mongo._colecao.delete_many({"cpf": entity.cpf})
            return True

        except Exception as e:
            raise Exception("Não foi possivel deletar o registro ", e)

    def listarTodos(self):
        try:
            query = list(self.mongo._colecao.find())

        except Exception as e:
            raise Exception("Erro ao consultar o registro ", e)

        return query

    def consultarId(self, id):

        try:
            query = self.mongo._colecao.find_one(ObjectId(id))

            if len(list(query)) == 0:
                raise Exception("Esse id não existe")

        except Exception as e:
            raise Exception("Erro ao consultar id (" + str(e) + ")")

        return query

    def atualizar(self, entity):
        try:
            query = self.mongo._colecao.replace_one({"cpf": entity.cpf}, entity.__dict__)
            return query

        except Exception as e:
            raise Exception("Erro ao atualizar o registro ", e)






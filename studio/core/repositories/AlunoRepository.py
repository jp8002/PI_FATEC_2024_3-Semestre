import logging
from datetime import datetime

import ipdb
from bson import ObjectId
from dns.e164 import query

from core.entity import AlunoEntity
from core.interfaces.InterfaceRepository import InterfaceRepository
from core.entity.AlunoEntity import Aluno

class AlunoRepository(InterfaceRepository):
    def __init__(self, mongo):
        self.mongo = mongo

    def criar(self,  entity):
        try:
            dados = entity.__dict__
            resp = self.mongo._colecao.insert_one(dados)

            return True

        except Exception as e:
            raise Exception("Não foi possivel criar o registro ", e)

    def consultarCpf(self, cpf):

        try:
            query = self.mongo._colecao.find_one({"cpf": cpf})
            list(query)

        except Exception as e:
            raise Exception("Esse cpf não existe (" + str(e) + ")")

        return query


    def deletarById(self, id):
        try:
            query = self.mongo._colecao.delete_many({"_id": ObjectId(id)})

            if(query.deleted_count == 0):
                raise Exception(f"Id: {id} não encontrada")

            return True

        except Exception as e:
            raise Exception("Não foi possivel deletar o registro ", e)


    def listarTodos(self):
        lista=[]
        try:
            query = list(self.mongo._colecao.find())

            for aluno in query:
                lista.append(Aluno(aluno))

        except Exception as e:
            raise Exception("Erro ao consultar o registro ", e)


        return lista

    def consultarId(self, id):
        query = self.mongo._colecao.find_one(ObjectId(id))

        if len(list(query)) == 0:
            raise Exception("Esse id não existe")

        return query

    def atualizar(self, entity):

        try:
            query = self.mongo._colecao.replace_one({"cpf": entity.cpf}, entity.__dict__)
            return query

        except Exception as e:
            raise Exception("Erro ao atualizar o registro ", e)
            return False

    def consultar_datas_agendadas(self):  # O METODO ATUALMENTE RETORNA TODAS AS DATAS (BASEADAS NAS ASSINATURAS ATIVAS) NO FORMATO DD/MM/AAAA
        datas_agendadas = []

        query = {"status": "ativo"}

        try:
            for cadastro in self.mongo._colecao.find(query):
                if "data_assinatura" in cadastro:
                    data_str = cadastro["data_assinatura"]
                    data_datetime = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
                    data = data_datetime.strftime("%d/%m/%Y")
                    datas_agendadas.append(data)

        except Exception as e:
            raise Exception("Erro ao consultar datas ", e)

        return datas_agendadas

    def agendar(self, Agendamento):
        id = Agendamento["id"]
        dia = Agendamento["dia"]

        alunoRepository = AlunoRepository(self.mongo)

        if (alunoRepository.consultarId(id) == False):
            raise Exception("Esse id não existe", id)

        try:
            dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")


        except Exception as e:
            raise Exception("Erro ao converter o dia ", e)

        try:
            self.mongo._colecao.update_one({"_id": ObjectId(id)}, {"$push": {"sessoes": dia}})


        except Exception as e:
            raise Exception("Erro ao atualizar dia ", e)

        return True

    def deletarAgendamento(self, Agendamento):
        cpf = Agendamento["cpf"]
        dia = Agendamento["dia"]

        alunoRepository = AlunoRepository(self.mongo)

        if (alunoRepository.consultarCpf(cpf) == False):
            raise Exception("Esse cpf não existe")

        try:
            dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")

        except Exception as e:
            raise Exception("Erro ao converter o dia ", e)

        try:
            self.mongo._colecao.update_one({"cpf": cpf}, {"$pull": {"sessoes": dia}})

        except Exception as e:
            raise Exception("Erro ao deletar agendamento ", e)

        return True

    def CriarTreinoAluno(self, idAluno, treino):
        try:
            treinoAdicao = self.mongo._colecao.update_one(
                {"_id": ObjectId(idAluno)},
                {"$push": {"treinos": treino}}
            )

            if treinoAdicao.modified_count == 0:
                raise Exception("Erro ao criar treino")
            return True

        except Exception as e:
            raise Exception(str(e))

    def deletarTreinoAluno(self, idAluno, treino):

        try:
            treinoRemocao = self.mongo._colecao.update_one(
                {"_id": ObjectId(idAluno)},
                {"$pull": {"treinos": treino}}
            )

            if treinoRemocao.modified_count == 0:
                raise Exception(f"Treino '{treino}' não encontrado para o Id {idAluno}")

            return True

        except Exception as e:
            raise Exception("Erro ao deletar treino: (" + str(e) + ")")


    def listarAlunosPorStatus(self, status):
        try:
            resp = self.mongo._colecao.find({"status": status})

            if not resp.next():
                raise Exception("Nenhum aluno encontrado.")

        except Exception as e:
            raise Exception("Erro ao listar alunos: (" + str(e) + ")")


        return resp
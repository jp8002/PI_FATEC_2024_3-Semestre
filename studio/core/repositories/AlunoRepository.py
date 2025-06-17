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
            #del dados['id']
            dados["data_nascimento"] = datetime.combine(dados["data_nascimento"], datetime.min.time())
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
        
    def deletarByCpf(self, cpf):
        try:
            query = self.mongo._colecao.delete_many({"cpf": cpf})

            if(query.deleted_count == 0):
                raise Exception(f"CPF: {cpf} não encontrado")

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
        query = self.mongo._colecao.find_one(ObjectId(id))

        if len(list(query)) == 0:
            raise Exception("Esse id não existe")

        return query

    def atualizar(self, entity):
        dados = entity.__dict__

        if '_id' in dados:
            del dados['_id']

        try:
            query = self.mongo._colecao.update_one({"cpf": entity.cpf}, {"$set": dados})
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
        exercicios = Agendamento["exercicios"]

        alunoRepository = AlunoRepository(self.mongo)

        if (alunoRepository.consultarId(id) == False):
            raise Exception("Esse id não existe", id)

        try:
            dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")


        except Exception as e:
            raise Exception("Erro ao converter o dia ", e)

        try:
                       #db.aluno.updateOne({ _id : ObjectId("id")}, {$push:{sessoes:{"dia":0,"exercicios":["xxx","yyy"]}}})
            self.mongo._colecao.update_one({"_id": ObjectId(id)}, {"$push":{"sessoes":{"dia":dia,"exercicios":exercicios}}})


        except Exception as e:
            raise Exception("Erro ao atualizar dia ", e)

        return True

    def deletarAgendamento(self, Agendamento):
        id = Agendamento["id"]
        dia = Agendamento["dia"]

        alunoRepository = AlunoRepository(self.mongo)

        alunoRepository.consultarId(id)


        try:
            dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")

        except Exception as e:
            raise Exception("Erro ao converter o dia ", e)

        try:
            self.mongo._colecao.update_one({"_id": ObjectId(id)}, {"$pull": {"sessoes":{ 'dia':dia}}})

        except Exception as e:
            raise Exception("Erro ao deletar agendamento ", e)

        return True

    def listarAlunosPorStatus(self, status):
        try:
            resp = self.mongo._colecao.find({"status": status})

            if not resp.next():
                raise Exception("Nenhum aluno encontrado.")

        except Exception as e:
            raise Exception("Erro ao listar alunos: (" + str(e) + ")")


        return resp

    def listarSessoes(self,id):
        try:
            resp = self.mongo._colecao.find_one({"_id": ObjectId(id)},{'_id':1,"sessoes":1,'nome':1})

            return resp

        except Exception as e:
            raise Exception("Erro ao listar sessoes: (" + str(e) + ")")

    def atualizarAgendamento(self, agendamento):
        id = ObjectId(agendamento['id'])

        dia = agendamento["dia"]
        dia = datetime.strptime(dia, "%Y-%m-%dT%H:%M")

        exercicios = agendamento["exercicios"]
        idSessao = agendamento["idSessao"]

        self.consultarId(agendamento["id"])



        try:
            self.mongo._colecao.update_one({'_id':id},{'$set':{f'sessoes.{idSessao}.dia':dia,
                                                               f'sessoes.{idSessao}.exercicios': exercicios
                                                               }})

        except Exception as e:
            raise Exception("Erro ao atualizar agendamento ", e)
    
    def TodosAlunosPorStatus(self):
        try:
            pipeline = [{'$group':{"_id":"$status","qtd":{"$sum":1}}},{'$sort':{'_id':1}}]
            return self.mongo._colecao.aggregate(pipeline).to_list()
        
        except Exception as e:
            raise Exception('Não foi possível agrupar alunos por status', e)
    
    def TodosAlunosPorPersonal(self):
        try:
            pipeline = [{"$group":{"_id":"$personal","qtd":{"$sum":1}}},{"$sort":{'_id':1}}]
            return self.mongo._colecao.aggregate(pipeline).to_list()

        except Exception as e:
            raise Exception('Não foi possível agrupar alunos por personal', e)

    def TodosAlunosPorPlano(self):
        try:
            pipeline = [{'$group':{'_id':'$plano','qtd':{'$sum':1}}},{'$sort':{'_id':1}}]
            return self.mongo._colecao.aggregate(pipeline).to_list()

        except Exception as e:
            raise Exception('Não foi possível agrupar alunos por plano', e)

    def tendenciaAssinatura(self):
        try:
            pipeline=[
                {
                    "$facet": {
                        "novas_assinaturas": [
                            {"$match": {"status": "ativo"}},
                            {"$project": {"mes": {"$month": "$data_assinatura"}}},
                            {"$group": {"_id": "$mes", "qtd": {"$sum": 1}}},
                            {"$sort": {"_id": 1}}
                        ],
                        "renovacoes": [
                            {"$match": {"status": "ativo"}},
                            {"$project": {"mes": {"$month": "$data_renovacao"}}},
                            {"$group": {"_id": "$mes", "qtd": {"$sum": 1}}},
                            {"$sort": {"_id": 1}}
                        ],
                        "cancelamentos": [
                            {"$match": {"status": "cancelado"}},
                            {"$project": {"mes": {"$month": "$data_cancelamento"}}},
                            {"$group": {"_id": "$mes", "qtd": {"$sum": 1}}},
                            {"$sort": {"_id": 1}}
                        ]
                    }
                }

            ]
            return self.mongo._colecao.aggregate(pipeline).next()
        except Exception as e:
            raise Exception('Não foi possível agrupar assinaturas', e)

    def alunoPorIdade(self):
        try:
            pipeline = [{'$group':{'_id':"$idade",'qtd':{'$sum':1}}},{'$sort':{'_id':1}}]
            return self.mongo._colecao.aggregate(pipeline).to_list()
        except Exception as e:
            raise Exception('Não foi possível agregar por idade', e)
        
    def AlterarStatus(self,novo_status, cpf):
            try:
                status_banco = "Ativo" if novo_status == "on" else "Cancelado"
                result = self.mongo._colecao.update_one(
                    {'cpf': cpf},
                    {'$set': {'status': status_banco}}
                )
                return result.modified_count > 0
            except Exception as e:
                raise Exception("Erro ao atualizar Status ", e)
                return False

    def alunoPorPersonal(self, personal):
        try:
            result = self.mongo._colecao.find({"personal":personal},{}).to_list()
        except Exception as e:
             raise Exception('Nenhum aluno encontrar', e)

        return result

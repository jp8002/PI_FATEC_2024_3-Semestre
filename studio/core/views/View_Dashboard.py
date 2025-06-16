import calendar

from django.views import View
from django.shortcuts import render, redirect
from core.services.ConexaoMongo import ConexaoMongo
from core.repositories.AlunoRepository import AlunoRepository


class DashboardView(View):
    def __init__(self):
        self.mongoClinte = ConexaoMongo()
        self.mongoClinte._colecao = self.mongoClinte._mydb["aluno"]
        self.alunoRepository = AlunoRepository(self.mongoClinte)

    def get(self,request):
        balancoAlunos = self.alunoRepository.TodosAlunosPorStatus().to_list()
        
        alunosPorPersonal = self.alunoRepository.TodosAlunosPorPersonal().to_list()
        for i in alunosPorPersonal:
            i["id"] = i.get("_id")

        alunosPorPlano = self.alunoRepository.TodosAlunosPorPlano().to_list()

        for i in alunosPorPlano:
            i["id"] = i.get("_id")

        tendenciaAssinaturas = self.alunoRepository.tendenciaAssinatura()
        novas ={}
        renovacoes = {}
        cancelados = {}

        for i in tendenciaAssinaturas['novas_assinaturas']:
            novas[i["_id"]] = i.get('qtd')

        for i in tendenciaAssinaturas['renovacoes']:
            renovacoes[i["_id"]] = i.get('qtd')

        for i in tendenciaAssinaturas['cancelamentos']:
            cancelados[i["_id"]] = i.get('qtd')

        tendenciaMeses = [
            {
                'mes' : calendar.month_name[i],
                'novas': novas.get(i,0),
                'renovacoes': renovacoes.get(i,0),
                'cancelados': cancelados.get(i,0)

            }
            for i in range(1,12)
        ]

        alunosPorIdade = self.alunoRepository.alunoPorIdade().to_list()
        for i in alunosPorIdade:
            i["idade"] = i.get("_id")

        context = {"balancoAlunos":balancoAlunos,
                    "alunosPorPersonal":alunosPorPersonal,
                    "alunosPorPlano":alunosPorPlano,
                   'tendenciaMeses':tendenciaMeses,
                   'alunosPorIdade':alunosPorIdade,
                   }

        return render(request, "TemplateTelaDashboard.html",context)


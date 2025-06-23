import calendar

from django.views import View
from django.shortcuts import render, redirect
from core.services.ConexaoMongo import ConexaoMongo
from core.repositories.AlunoRepository import AlunoRepository
from core.services.MontarTendencias import montarTendencias
from core.services.convert_id import convert_idTo
from core.services.Autenticar import Autenticar


class DashboardView(View):
    def __init__(self):
        self.mongoClinte = ConexaoMongo()
        self.mongoClinte._colecao = self.mongoClinte._mydb["aluno"]
        self.alunoRepository = AlunoRepository(self.mongoClinte)

    def get(self,request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        
        if not Autenticar.checarAdmin(request.session):
            return redirect("paginaInicial")
        
        balancoAlunos = self.alunoRepository.TodosAlunosPorStatus()
        
        alunosPorPersonal = self.alunoRepository.TodosAlunosPorPersonal()
        convert_idTo('id', alunosPorPersonal)


        alunosPorPlano = self.alunoRepository.TodosAlunosPorPlano()
        convert_idTo('id', alunosPorPlano)

        tendenciaAssinaturas = self.alunoRepository.tendenciaAssinatura()


        alunosPorIdade = self.alunoRepository.alunoPorIdade()
        convert_idTo('idade', alunosPorIdade)

        context = {"balancoAlunos":balancoAlunos,
                    "alunosPorPersonal":alunosPorPersonal,
                    "alunosPorPlano":alunosPorPlano,
                   'tendenciaMeses':montarTendencias(tendenciaAssinaturas),
                   'alunosPorIdade':alunosPorIdade,
                   }

        return render(request, "TemplateTelaDashboard.html",context)


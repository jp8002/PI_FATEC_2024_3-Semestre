import ipdb
from django.shortcuts import redirect, render
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.services.sequenciaTolista import sequenciaTolista


class AgendarTreinoView(View):

    def __init__(self):
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM._mydb["aluno"]

        self.alunoRepository = AlunoRepository(self.serviceM)

    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        listaAlunos = self.alunoRepository.listarTodos()


        contexto = {'alunos': listaAlunos}

        return render(request, "TemplateAgendarTreino.html", contexto)

    def post(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        agendamento = request.POST.dict()

        # agendamento["exercicios"] = agendamento["exercicios"].split(";")
        agendamento["exercicios"] = sequenciaTolista.strTolista(agendamento["exercicios"])

        self.alunoRepository.agendar(agendamento)

        listaAlunos = self.alunoRepository.listarTodos()

        contexto = {'alunos': listaAlunos}

        return redirect("agendarTreino")
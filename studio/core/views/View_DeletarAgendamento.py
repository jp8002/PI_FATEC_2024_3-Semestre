from django.shortcuts import redirect, render
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.service import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class DeletarAgendamentoView(View):

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

        return render(request, "TemplateDeletarAgendamento.html", contexto)

    def post(self, request):

        agendamento = request.POST.dict()

        self.alunoRepository.deletarAgendamento(agendamento)

        listaAlunos = self.alunoRepository.listarTodos()

        contexto = {'alunos': listaAlunos}

        return render(request, "TemplateDeletarAgendamento.html", contexto)
from django.shortcuts import redirect, render
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class ListarAlunosView(View):
    
    def __init__(self, ):
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM._mydb["aluno"]
        self.alunoRepository = AlunoRepository(self.serviceM)


    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")


        listaAlunos = self.alunoRepository.listarTodos()
        total_alunos = len(listaAlunos)

        contexto = {
            'alunos': listaAlunos,
            'total_alunos': total_alunos
        }

        return render(request, "TemplateListarAlunos.html", contexto)
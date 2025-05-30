from django.shortcuts import redirect, render
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar, ConexaoMongo


class AlunoInicialView(View):
    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        cpf = request.session.get("cpf", False)
        serviceM = ConexaoMongo()

        serviceM._colecao = serviceM._mydb["aluno"]

        repository = AlunoRepository(serviceM)

        aluno = repository.consultarCpf(cpf)

        contexto = {'aluno': aluno}

        return render(request, "TemplateAlunoInicial.html", contexto)
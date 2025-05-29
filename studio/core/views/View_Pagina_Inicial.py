from django.shortcuts import render, redirect
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.service import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class PaginaInicialView(View):

    def get(self, request):
        if Autenticar.checarSessaoPersonal(request.session):
            return redirect("personalInicial")

        contexto = {}

        if Autenticar.checarSessao(request.session):
            cpf = request.session.get("cpf", False)
            serviceM = ConexaoMongo()

            serviceM._colecao = serviceM._mydb["aluno"]

            alunoRepository = AlunoRepository(serviceM)

            aluno = alunoRepository.consultarCpf(cpf)

            contexto = {'aluno': aluno}

        return render(request, "TemplatePaginaInicial.html", contexto)
from django.views import View
from django.shortcuts import redirect, render

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class AlunoPersonalView(View):
    def __init__(self):
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM._mydb["aluno"]


    def get(self,request,nome):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        alunoRepo = AlunoRepository(self.serviceM)

        context = {
            "alunos":alunoRepo.alunoPorPersonal(nome),
            'total_aluno':len(alunoRepo.alunoPorPersonal(nome)),
        }

        return render(request, "TemplateAlunoPersonal.html", context)



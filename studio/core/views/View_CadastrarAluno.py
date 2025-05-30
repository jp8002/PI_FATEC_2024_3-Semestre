from django.shortcuts import redirect, render
from django.views import View

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class CadastrarAlunoView(View):
    def get(self, request):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")


        return render(request, "TemplateCadastrarAluno.html")


    def post(self, request):
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["aluno"]

        aluno = Aluno(request.POST)

        repository = AlunoRepository(serviceM)

        repository.criar(aluno)
        return render(request, "TemplateCadastrarAluno.html")

from django.shortcuts import redirect, render
from django.views import View
from datetime import datetime

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarAlunoForm


class CadastrarAlunoView(View):
    def get(self, request):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")

        form = CadastrarAlunoForm()
        return render(request, "TemplateCadastrarAluno.html", {'form':form})


    def post(self, request):
        form = CadastrarAlunoForm(request.POST)
        if form.is_valid():
            serviceM = ConexaoMongo()
            serviceM._colecao = serviceM._mydb["aluno"]
            dados = (form.cleaned_data) 
            dados["status"] = "Ativo"
            dados["data_assinatura"] = datetime.now()
            dados['idade'] =  datetime.now().year - dados['data_nascimento'].year

            aluno = Aluno(dados)

            repository = AlunoRepository(serviceM)

            repository.criar(aluno)
            return redirect('cadastrarAluno')

        return render(request, "TemplateCadastrarAluno.html", {'errors':form.errors})

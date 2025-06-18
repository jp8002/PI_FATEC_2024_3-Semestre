from django.shortcuts import redirect, render
from django.views import View
from datetime import datetime

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarAlunoForm

class EditarAlunoView(View):
    def get(self, request, cpf):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")
        
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["aluno"]
        repository = AlunoRepository(serviceM)
        
        aluno = repository.consultarCpf(cpf)
        if not aluno:
            return redirect("listarAlunos")
        
        form = CadastrarAlunoForm(initial=aluno)
        return render(request, "TemplateEditarAluno.html", {'form': form, 'cpf': cpf})
    
    def post(self, request, cpf):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")
        
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["aluno"]
        repository = AlunoRepository(serviceM)

        aluno_existente = repository.consultarCpf(cpf)
        
        form = CadastrarAlunoForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            dados["data_nascimento"] = datetime.combine(dados["data_nascimento"], datetime.min.time())

            aluno = Aluno(dados)
            aluno.status = aluno_existente.get('status')
            aluno.data_assinatura = aluno_existente.get('data_assinatura')
            aluno.data_renovacao = aluno_existente.get('data_renovacao')
            aluno.sessoes = aluno_existente.get('sessoes')
            
            repository.atualizar(aluno)
            return redirect("listarAlunos")
        
        return render(request, "TemplateEditarAluno.html", {'form': form, 'cpf': cpf})
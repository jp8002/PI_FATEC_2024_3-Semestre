
from django.shortcuts import redirect, render
from django.views import View
from datetime import datetime

from core.entity.AlunoEntity import Aluno
from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarAlunoForm

class EditarAlunoView(View):
    def __init__(self):
        super().__init__()
        self.form = None
        self.errors = None
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM.mydb["aluno"]
        self.repository = AlunoRepository(self.serviceM)


    def get(self, request, cpf):
        aluno = None
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")

        try:
            aluno = self.repository.consultarCpf(cpf)
            if not aluno:
                return redirect("listarAlunos")

        except Exception as e:
            self.errors = e

        if not self.form:
         self.form = CadastrarAlunoForm(initial=aluno)


        context = {"errors": self.errors, 'form': self.form, 'cpf': cpf}

        return render(request, "TemplateEditarAluno.html", context)
    
    def post(self, request, cpf):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")

        aluno_existente = self.repository.consultarCpf(cpf)
        
        self.form = CadastrarAlunoForm(request.POST)

        if self.form.is_valid():

            dados = self.form.cleaned_data
            dados["data_nascimento"] = datetime.combine(dados["data_nascimento"], datetime.min.time())

            aluno = Aluno(dados)
            aluno.status = aluno_existente.get('status')
            aluno.data_assinatura = aluno_existente.get('data_assinatura')
            aluno.data_renovacao = aluno_existente.get('data_renovacao')
            aluno.sessoes = aluno_existente.get('sessoes')
            aluno.idade = aluno_existente.get('idade')


            self.repository.atualizar(aluno)
            return redirect("listarAlunos")

        return self.get(request, cpf)
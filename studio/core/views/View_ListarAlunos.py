from django.shortcuts import redirect, render
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarAlunoForm
from core.services.convert_id import convert_idTo


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
        convert_idTo("id",listaAlunos)
        form = CadastrarAlunoForm()

        contexto = {
            'alunos': listaAlunos,
            'total_alunos': total_alunos,
            'form': form
        }

        return render(request, "TemplateListarAlunos.html",contexto)
    
    def post(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        action = request.POST.get("action",None)

        if action == "excluir":
            self.alunoRepository.deletarByCpf(request.POST['cpf'])
            return redirect("listarAlunos")

        if 'cpf' in request.POST and 'status' in request.POST:
            self.alunoRepository.AlterarStatus(
                request.POST['status'],cpf=request.POST['cpf']

        )
        elif 'cpf' in request.POST and 'status' not in request.POST:
            status = 'off'
            self.alunoRepository.AlterarStatus(
                status,
                request.POST['cpf']
            )
        return redirect('listarAlunos')
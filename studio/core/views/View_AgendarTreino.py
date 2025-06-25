
from django.shortcuts import redirect, render
from django.views import View

from core.forms import AgendamentoForm
from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.services.sequenciaTolista import sequenciaTolista


class AgendarTreinoView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM.mydb["aluno"]

        self.listaAlunos = None
        self.errors = None
        self.alunoRepository = AlunoRepository(self.serviceM)

    def get(self, request):

        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        try:
            self.listaAlunos = self.alunoRepository.listarTodos()
        except Exception as e:
            self.errors = e

        contexto = {'alunos': self.listaAlunos, "errors": self.errors}

        return render(request, "TemplateAgendarTreino.html", contexto)

    def post(self, request):
        errors = None
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        form = AgendamentoForm(request.POST)

        if form.is_valid():
            try:
                agendamento = request.POST.dict()

                agendamento["exercicios"] = sequenciaTolista.strTolista(agendamento["exercicios"])

                self.alunoRepository.agendar(agendamento)

                return redirect("agendarTreino")
            except Exception as e:
                self.errors = e

        self.listaAlunos = self.alunoRepository.listarTodos()

        contexto = {'alunos': self.listaAlunos,
                    "form": form,
                    "errors": errors}

        return  render (request, "TemplateAgendarTreino.html", contexto)
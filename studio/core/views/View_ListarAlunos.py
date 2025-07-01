
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarAlunoForm



class ListarAlunosView(View):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM.mydb["aluno"]
        self.alunoRepository = AlunoRepository(self.serviceM)



    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        page = int(request.GET.get('page', 1))
        pesquisaNome = request.GET.get('pesquisaNome', "")
        ordemAlunos = request.GET.get('ordemAlunos',"crescente")
        errors = []

        try:
            alunos = self.alunoRepository.listarTodosPorInicioNome(pesquisaNome).to_list()

            if ordemAlunos == "crescente":
                alunos.sort(key=lambda a: a["nome"])
            elif ordemAlunos == "decrescente":
                alunos.sort(key=lambda a: a["nome"], reverse=True)

            total_alunos = len(alunos)

            p = Paginator(alunos, 10)
            pagina = p.get_page(page)
        except Exception as e:
            pagina = []
            total_alunos = None
            errors = e

        contexto = {
            "pesquisaNome": pesquisaNome,
            "ordemAlunos" : ordemAlunos,
            'alunos': pagina,
            'total_alunos': total_alunos,
            'form': CadastrarAlunoForm(),
            "errors": errors
        }

        return render(request, "TemplateListarAlunos.html",contexto)
    
    def post(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        try:
            action = request.POST.get("action",None)

            match action:
                case "excluir":
                    self.alunoRepository.deletarByCpf(request.POST['cpf'])
                    return redirect("listarAlunos")

                case"Z-A":
                    return redirect(f"{request.path}?pesquisaNome={request.GET.get('pesquisaNome',"")}&ordemAlunos=decrescente")

                case "A-Z":
                    return redirect(f"{request.path}?pesquisaNome={request.GET.get('pesquisaNome',"")}&ordemAlunos=crescente")

                case "pesquisar":
                    return redirect(f"{request.path}?pesquisaNome={request.POST['pesquisaNome']}&ordemAlunos={request.GET.get('ordemAlunos','crescente')}")


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

        except Exception as e:
            self.errors = e


        return self.get(request)



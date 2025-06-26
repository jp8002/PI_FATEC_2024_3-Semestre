
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import redirect, render

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class AlunoPersonalView(View):
    def __init__(self):

        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM.mydb["aluno"]
        self.alunoRepo = AlunoRepository(self.serviceM)

    def get(self,request,personal):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarAdmin(request.session):
            return redirect("paginaInicial")
        
        pesquisaNome = request.GET.get("pesquisaNome","")
        errors = []
        page = request.GET.get('page',1)
        ordemAlunos = request.GET.get('ordemAlunos',"crescente")

        try:
            alunos = self.alunoRepo.alunoPorPersonalENome(personal, pesquisaNome)
            if ordemAlunos == "crescente":
                alunos.sort(key=lambda aluno: aluno['nome'])
            else:
                alunos.sort(key=lambda aluno: aluno['nome'],reverse=True)

            total_alunos = len(alunos)
            p = Paginator(alunos,10)
            pagina_de_alunos = p.page(page)
        except Exception as e:
            pagina_de_alunos = []
            total_alunos = 0
            alunos = []
            errors = e

        context = {
            "personal": personal,
            'total_aluno':total_alunos,
            "pesquisaNome": pesquisaNome,
            "errors":errors,
            "pagina_de_alunos":pagina_de_alunos,
            "ordemAlunos":ordemAlunos,
        }

        return render(request, "TemplateAlunoPersonal.html", context)

    def post(self,request,personal):

        action = request.POST.get('action','')

        if action == 'Z-A':
            return redirect(f"{request.path}?ordemAlunos=decrescente")

        elif action == 'A-Z':\
            return redirect(f"{request.path}?ordemAlunos=crescente")

        elif action == "pesquisar":
            return redirect(f"{request.path}?pesquisaNome={request.POST.get('pesquisaNome')}")


        return redirect("paginaInicial")



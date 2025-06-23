from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.shortcuts import redirect, render
from django.views import View

from core.repositories.PersonalRepository import PersonalRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class ListarPersonalView(View):

    def __init__(self, **kwargs):
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM._mydb["personal"]
        self.personalRepository = PersonalRepository(self.serviceM)

    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        pesquisaNome = request.GET.get("pesquisaNome","")
        page = request.GET.get("page",1)
        errors = []
        ordemPersonais = request.GET.get("ordemPersonais","crescente")

        try:
            personais = self.personalRepository.listarTodosPorInicioNome(pesquisaNome).to_list()

            if ordemPersonais == "crescente":
                personais.sort(key=lambda x: x["nome"])

            elif ordemPersonais == "decrescente":
                personais.sort(key=lambda x: x["nome"], reverse=True)


            total_personal = len(personais)
            p = Paginator(personais, per_page=10)
            paginas_de_personais = p.page(page)

        except Exception as e:
            personais = None
            total_personal = 0
            errors = e
            paginas_de_personais = []

        contexto = {
            'paginas_de_personais': paginas_de_personais,
            'total_personal': total_personal,
            "errors": errors,
            "ordemPersonais": ordemPersonais,
            "pesquisaNome": pesquisaNome,
        }

        return render(request, "TemplateListarPersonal.html", contexto)

    def post(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        action = request.POST.get("action",None)

        if action == "excluir":
            self.personalRepository.deletarByCpf(request.POST.get("cpf"))
            return redirect("listarPersonal")

        if action == "Z-A":
            return redirect(f"{request.path}?ordemPersonais=decrescente")

        if action == "A-Z":
            return redirect(f"{request.path}?ordemPersonais=crescente")

        if action == "pesquisar":
            return redirect(f"{request.path}?pesquisaNome={request.POST.get('pesquisaNome')}")

        return redirect("paginaInicial")
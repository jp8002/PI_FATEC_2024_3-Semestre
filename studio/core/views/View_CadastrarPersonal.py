from django.shortcuts import redirect, render
from django.views import View
from core.entity.PersonalEntity import PersonalEntity
from core.repositories.PersonalRepository import PersonalRepository

from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarPersonalForm


class CadastrarPersonalView(View):
    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        
        if not Autenticar.checarAdmin(request.session):
            return redirect("paginaInicial")

        return render(request, "TemplateCadastrarPersonal.html")

    def post(self, request):
        if not Autenticar.checarAdmin(request.session):
            return redirect("paginaInicial")
        
        form = CadastrarPersonalForm(request.POST)

        if form.is_valid():
            serviceM = ConexaoMongo()
            serviceM._colecao = serviceM.mydb["personal"]
            personal = PersonalEntity(form.cleaned_data)
            personal_repository = PersonalRepository(serviceM)
            personal_repository.criar(personal)
            # serviceM.criarNovoPersonal(request.POST.get('nome'), request.POST.get('senha'),
            #                            request.POST.get('telefone'), request.POST.get('email'), request.POST.get('cpf'),
            #                            request.POST.get('salario'), request.POST.get('acesso'),
            #                            request.POST.get('cref'))
            return redirect("cadastrarPersonal")
        else:
            context={'errors':form.errors}
            #raise Exception(form.errors)
            return render(request, "TemplateCadastrarPersonal.html", context)
        
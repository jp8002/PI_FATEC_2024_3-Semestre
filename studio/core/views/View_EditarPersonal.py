from django.shortcuts import redirect, render
from django.views import View

from core.entity.PersonalEntity import PersonalEntity
from core.repositories.PersonalRepository import PersonalRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from core.forms import CadastrarPersonalForm

class EditarPersonalView(View):
    def get(self, request, cpf):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")
        
        if not Autenticar.checarAdmin(request.session):
            return redirect("paginaInicial")
        
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["personal"]
        repository = PersonalRepository(serviceM)
        
        personal = repository.consultarCpf(cpf)
        if not personal:
            return redirect("listarPersonal")
        
        form = CadastrarPersonalForm(initial=personal)
        return render(request, "TemplateEditarPersonal.html", {'form': form, 'cpf': cpf})
    
    def post(self, request, cpf):
        sessao = request.session
        if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
            return redirect("paginaInicial")
        
        if not Autenticar.checarAdmin(request.session):
            return redirect("paginaInicial")
        
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["personal"]
        repository = PersonalRepository(serviceM)

        form = CadastrarPersonalForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            
            personal = PersonalEntity(dados)
            
            repository.atualizar(personal)
            return redirect("listarPersonal")
        
        return render(request, "TemplateEditarPersonal.html", {'form': form, 'cpf': cpf})
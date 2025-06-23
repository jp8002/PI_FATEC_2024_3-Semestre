from django.shortcuts import redirect, render
from django.views import View

from core.repositories.PersonalRepository import PersonalRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class PersonalInicialView(View):
    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        
        if Autenticar.checarAdmin(request.session):
            acesso = 'adm'
        else:
            acesso = 'funcionario'

        cpf = request.session.get("cpf", False)
        serviceM = ConexaoMongo()

        serviceM._colecao = serviceM._mydb["personal"]

        personalRepository = PersonalRepository(serviceM)

        personal = personalRepository.consultarCpf(cpf)

        contexto = {'personal': personal, 'acesso': acesso}

        return render(request, "TemplatePersonalInicial.html", contexto)
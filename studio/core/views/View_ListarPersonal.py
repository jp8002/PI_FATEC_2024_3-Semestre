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

        listaPersonal = self.personalRepository.listarTodos().to_list()
        total_personal = len(listaPersonal)

        contexto = {
            'personais': listaPersonal,
            'total_personal': total_personal
        }

        return render(request, "TemplateListarPersonal.html", contexto)
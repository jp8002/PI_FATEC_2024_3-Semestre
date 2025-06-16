from django.shortcuts import render, redirect
from django.views import View

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class PaginaInicialView(View):

    def get(self, request):

        if Autenticar.checarSessao(request.session):
            return redirect("personalInicial")

        return render(request, "TemplatePaginaInicial.html", )
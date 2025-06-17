from django.shortcuts import redirect, render
from django.views import View

from core.repositories.PersonalRepository import PersonalRepository
from core.services.AutenticadorUsuario import AutenticadorUsuario
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo


class LoginView(View):
    def __init__(self):
        self.conexao = ConexaoMongo()
        self.conexao._colecao = self.conexao._mydb["personal"]
        self.personalRepo = PersonalRepository(self.conexao)
        self.autenticador = AutenticadorUsuario(self.personalRepo)

    def get(self, request):
        if  Autenticar.checarSessao(request.session):
            return redirect("personalInicial")


        return render(request, "TemplateLogin.html")

    def post(self, request):
        usuario = request.POST

        if not self.autenticador.AutenticarUsuario(usuario):
            return render(request, "TemplateLogin.html")

        request.session["sessao"] = True
        request.session["cpf"] = usuario.get("cpf")
        
        return redirect("paginaLogin")

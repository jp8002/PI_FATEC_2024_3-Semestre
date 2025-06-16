from django.shortcuts import redirect, render
from django.views import View

from core.services.Autenticar import Autenticar


class LoginView(View):
    def get(self, request):
        if  Autenticar.checarSessao(request.session):
            return redirect("personalInicial")


        return render(request, "TemplateLogin.html")

    def post(self, request):
        usuario = request.POST

        if not Autenticar.AuthUsuario(usuario):
            return render(request, "TemplateLogin.html")

        request.session["sessao"] = True
        request.session["cpf"] = usuario.get("cpf")
        
        return redirect("paginaLogin")

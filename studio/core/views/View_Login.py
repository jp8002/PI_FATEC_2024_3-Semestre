from django.shortcuts import redirect, render
from django.views import View

from core.services.Autenticar import Autenticar


class LoginView(View):
    def get(self, request):
        if Autenticar.checarSessaoAluno(request.session):
            return redirect("alunoInicial")
        elif Autenticar.checarSessaoPersonal(request.session):
            return redirect("personalInicial")

        if (request.method == "GET"):
            return render(request, "TemplateLogin.html")

    def post(self, request):
        usuario = request.POST

        if not Autenticar.AuthUsuario(usuario):
            return render(request, "TemplateLogin.html")

        request.session["sessao"] = True
        request.session["cpf"] = usuario.get("cpf")
        request.session["tipo_usuario"] = usuario.get("tipo_usuario")

        return redirect("paginaLogin")

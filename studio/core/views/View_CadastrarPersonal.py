from django.shortcuts import redirect, render
from django.views import View

from core.services.Autenticar import Autenticar
from core.services import ConexaoMongo


class CadastrarPersonalView(View):
    def get(self, request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        return render(request, "TemplateCadastrarPersonal.html")

    def post(self, request):
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["personal"]
        serviceM.criarNovoPersonal(request.POST.get('nome'), request.POST.get('senha'),
                                   request.POST.get('telefone'), request.POST.get('email'), request.POST.get('cpf'),
                                   request.POST.get('salario'), request.POST.get('acesso'),
                                   request.POST.get('cref'))

        return render(request, "TemplateCadastrarPersonal.html")
from django.shortcuts import redirect, render
from django.views import View

from core.services.Autenticar import Autenticar
from core.services import ConexaoMongo



class AtualizarPersonalView(View):

    def __init__(self, agendamento):
        self.serviceM = ConexaoMongo()
        self.serviceM._colecao = self.serviceM._mydb["personal"]

    def get(self,request):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")

        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        listaPersonal = self.serviceM.listarPersonals()

        contexto = {'personals': listaPersonal}

        return render(request, "TemplateAtualizarPersonal.html", contexto)

    def post(self,request):
            atualizacao = request.POST.dict()
            self.serviceM.atualizarPersonal(atualizacao["cpf"], atualizacao["telefone"], atualizacao["email"],
                                            atualizacao["salario"], atualizacao["acesso"])

            listaPersonal = self.serviceM.listarPersonals()

            contexto = {'personals': listaPersonal}

            return render(request, "TemplateAtualizarPersonal.html", contexto)
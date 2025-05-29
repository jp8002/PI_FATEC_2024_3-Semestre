from django.shortcuts import render
from django.views import View

from core.services import ConexaoMongo


class CalendarioViews(View):

    def get(request):
        serviceM = ConexaoMongo()

        serviceM._colecao = serviceM._mydb["aluno"]

        datas = serviceM.consultar_datas_agendadas()
        contexto = {'datas': datas}

        return render(request, "TemplateCalendario.html", contexto)
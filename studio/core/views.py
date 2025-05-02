from django.shortcuts import render, redirect
import pymongo

import ipdb
from core.services import ServiceMongo
from core.services import Autenticar

# Create your views here.
def View_Pagina_Inicial(request):
    contexto={}
    
    if Autenticar.checarSessao(request.session):
        rg = request.session.get("rg", False)
        serviceM = ServiceMongo()
       
        serviceM._colecao = serviceM._mydb["clientes"]
        
        cliente = serviceM.consultarRg(rg)
        
        contexto={'cliente':cliente}
        
    #ipdb.set_trace()
    
    return render(request, "TemplatePaginaInicial.html",contexto)
    
def Calendario(request):
    contexto={}
    serviceM = ServiceMongo()

    serviceM._colecao = serviceM._mydb["clientes"]

    datas = serviceM.consultar_datas_agendadas()
    contexto={'datas':datas}

    return render(request, "TemplateCalendario.html", contexto)


def View_Login(request):
    if Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")

    if(request.method == "GET"):
        return render(request, "TemplateLogin.html")
    
    usuario = request.POST
    
    if not Autenticar.AuthUsuario(usuario):
        return render(request, "TemplateLogin.html")
    
    request.session["sessao"] = True
    request.session["rg"] = usuario.get("rg")
    
    return redirect("paginaInicial")
    
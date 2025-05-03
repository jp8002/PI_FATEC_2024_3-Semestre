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
    if Autenticar.checarSessaoCliente(request.session):
        return redirect("alunoInicial")
    elif Autenticar.checarSessaoPersonal(request.session):
        return redirect("personalInicial")
    #ipdb.set_trace()
    if(request.method == "GET"):
        return render(request, "TemplateLogin.html")
    
    usuario = request.POST
    
    if not Autenticar.AuthUsuario(usuario):
        return render(request, "TemplateLogin.html")
    
    request.session["sessao"] = True
    request.session["rg"] = usuario.get("rg")
    request.session["cpf"] = usuario.get("cpf")
    
    return redirect("paginaInicial")


def View_AlunoInicial(request):
    
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    rg = request.session.get("rg", False)
    serviceM = ServiceMongo()
    
    serviceM._colecao = serviceM._mydb["clientes"]
    
    cliente = serviceM.consultarRg(rg)
    
    contexto={'cliente':cliente}
    
    
    return render(request, "TemplateAlunoInicial.html", contexto)

def View_PersonalInicial(request):
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    cpf = request.session.get("cpf", False)
    serviceM = ServiceMongo()

    serviceM._colecao = serviceM._mydb["personals"]

    personal = serviceM.consultarCpf(cpf)

    contexto={'personal':personal}


    return render(request, "TemplatePersonalInicial.html", contexto)

def View_CadastrarPersonal(request):
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")

    if request.method == 'POST':
        serviceM = ServiceMongo()
        serviceM._colecao = serviceM._mydb["personals"]
        serviceM.criarNovoPersonal(request.POST.get('nome'),request.POST.get('senha'),request.POST.get('telefone'),request.POST.get('email'),request.POST.get('cpf'),request.POST.get('salario'))

    return render(request, "TemplateCadastrarPersonal.html")
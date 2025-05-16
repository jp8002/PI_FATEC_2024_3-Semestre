import datetime
from django.shortcuts import render, redirect
import pymongo

import ipdb
from core.services import ServiceMongo
from core.services import Autenticar

# Create your views here.
def View_Pagina_Inicial(request):

    if Autenticar.checarSessaoPersonal(request.session):
        return redirect("personalInicial")

    contexto={}

    if Autenticar.checarSessao(request.session):
        cpf = request.session.get("cpf", False)
        serviceM = ServiceMongo()

        serviceM._colecao = serviceM._mydb["aluno"]

        aluno = serviceM.consultarCpf(cpf)

        contexto={'aluno':aluno}
        
    #ipdb.set_trace()

    return render(request, "TemplatePaginaInicial.html",contexto)
    
def Calendario(request):
    contexto={}
    serviceM = ServiceMongo()

    serviceM._colecao = serviceM._mydb["aluno"]

    datas = serviceM.consultar_datas_agendadas()
    contexto={'datas':datas}

    return render(request, "TemplateCalendario.html", contexto)


def View_Login(request):
    if Autenticar.checarSessaoAluno(request.session):
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
    request.session["cpf"] = usuario.get("cpf")
    request.session["tipo_usuario"] = usuario.get("tipo_usuario")

    return redirect("paginaLogin")


def View_AlunoInicial(request):
    
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    cpf = request.session.get("cpf", False)
    serviceM = ServiceMongo()
    
    serviceM._colecao = serviceM._mydb["aluno"]
    
    aluno = serviceM.consultarCpf(cpf)
    
    contexto={'aluno':aluno}
    
    
    return render(request, "TemplateAlunoInicial.html", contexto)

def View_PersonalInicial(request):
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    cpf = request.session.get("cpf", False)
    serviceM = ServiceMongo()

    serviceM._colecao = serviceM._mydb["personal"]

    personal = serviceM.consultarCpf(cpf)

    contexto={'personal':personal}


    return render(request, "TemplatePersonalInicial.html", contexto)

def View_CadastrarPersonal(request):
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")

    if request.method == 'POST':
        serviceM = ServiceMongo()
        serviceM._colecao = serviceM._mydb["personal"]
        serviceM.criarNovoPersonal(request.POST.get('nome'),request.POST.get('senha'),request.POST.get('telefone'),request.POST.get('email'),request.POST.get('cpf'),request.POST.get('salario'),request.POST.get('acesso'),request.POST.get('cref'))

    return render(request, "TemplateCadastrarPersonal.html")


def View_CadastrarAluno(request):
    sessao = request.session
    if not Autenticar.checarSessao(sessao) or not Autenticar.checarSessaoPersonal(sessao):
        #ipdb.set_trace()
        return redirect("paginaInicial")

    if request.method == 'GET':
        return render(request, "TemplateCadastrarAluno.html")

    serviceM = ServiceMongo()
    serviceM._colecao = serviceM._mydb["aluno"]

    serviceM.CriarNovoAluno(request.POST)
    return render(request, "TemplateCadastrarAluno.html")


def View_AgendarTreino(request):
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")

    if not Autenticar.checarSessaoPersonal(request.session):
        return redirect("paginaInicial")

    serviceM = ServiceMongo()
    serviceM._colecao = serviceM._mydb["aluno"]

    if request.method == 'POST':
        agendamento = request.POST.dict()
        serviceM.agendar(agendamento)

    listaAlunos = serviceM.listarAlunos()

    contexto = {'alunos': listaAlunos}

    return render(request, "TemplateAgendarTreino.html", contexto)

def View_DeletarAgendamento(request): # QUAL TELA ESSAS FUNÇÕES FAZEM PARTE???~KPO
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")

    if not Autenticar.checarSessaoPersonal(request.session):
        return redirect("paginaInicial")

    serviceM = ServiceMongo()
    serviceM._colecao = serviceM._mydb["aluno"]

    if request.method == 'POST':
        agendamento = request.POST.dict()
        serviceM.deletarAgendamento(agendamento)

    listaAlunos = serviceM.listarAlunos()

    contexto = {'alunos': listaAlunos}

    return render(request, "TemplateDeletarAgendamento.html", contexto)

def View_CriarTreinoAluno(request): # QUAL TELA ESSAS FUNÇÕES FAZEM PARTE???~KPO
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    if not Autenticar.checarSessaoPersonal(request.session):
        return redirect("paginaInicial")
    
    serviceM = ServiceMongo()
    serviceM._colecao = serviceM._mydb["aluno"]

    if request.method == 'POST':
        agendamento = request.POST.dict()
        serviceM.CriarTreinoAluno(agendamento["cpf"],agendamento["treino"])

    listaAlunos = serviceM.listarAlunos()

    contexto = {'alunos': listaAlunos}

    return render(request, "TemplateCriarTreino.html", contexto)

def View_DeletarTreinoAluno(request): # QUAL TELA ESSAS FUNÇÕES FAZEM PARTE???~KPO
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    if not Autenticar.checarSessaoPersonal(request.session):
        return redirect("paginaInicial")
    
    serviceM = ServiceMongo()
    serviceM._colecao = serviceM._mydb["aluno"]

    if request.method == 'POST':
        agendamento = request.POST.dict()
        serviceM.deletarTreinoAluno(agendamento["cpf"],agendamento["treino"])

    listaAlunos = serviceM.listarAlunos()

    contexto = {'alunos': listaAlunos}

    return render(request, "TemplateDeletarTreino.html", contexto)

def View_AtualizarPersonal(request):
    if not Autenticar.checarSessao(request.session):
        return redirect("paginaInicial")
    
    if not Autenticar.checarSessaoPersonal(request.session):
        return redirect("paginaInicial")
    
    serviceM = ServiceMongo()
    serviceM._colecao = serviceM._mydb["personal"]

    if request.method == 'POST':
        atualizacao = request.POST.dict()
        serviceM.atualizarPersonal(atualizacao["cpf"],atualizacao["telefone"],atualizacao["email"],atualizacao["salario"],atualizacao["acesso"])

    listaPersonal = serviceM.listarPersonals()

    contexto = {'personals': listaPersonal}

    return render(request, "TemplateAtualizarPersonal.html", contexto)
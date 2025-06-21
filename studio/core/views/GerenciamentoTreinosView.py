from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render, redirect
from pygments.styles.rainbow_dash import RED_BRIGHT

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo

from core.services.sequenciaTolista import sequenciaTolista


class GerenciamentoTreinosView(View):
    def __init__(self,**kwargs):

        self.mongoClinte = ConexaoMongo()
        self.mongoClinte._colecao = self.mongoClinte._mydb["aluno"]

        self.alunoRepository = AlunoRepository(self.mongoClinte)
        self.listaSessoes = kwargs.get("listaSessoes",None)

    def get(self,request,cpf,**kwargs):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        if not request.GET.get('dataEscolhida') :
            self.listaSessoes = self.alunoRepository.listarSessoes(cpf)
        else:
            self.listaSessoes = self.alunoRepository.listarSessaoPorDia(cpf,request.GET.get('dataEscolhida'))



        for index, i in enumerate(self.listaSessoes.get('sessoes')):
            i["idSessao"] = index
            i['dia'] = i.get('dia').strftime("%Y-%m-%dT%H:%M")
            i['exerciciosList'] = ';\n'.join(i.get('exercicios'))


        self.listaSessoes["sessoes"] = sorted(self.listaSessoes["sessoes"], key=lambda k: k['dia'])

        p = Paginator(self.listaSessoes.get('sessoes'), 1)
        page = request.GET.get('page')


        sessoes = p.get_page(page)

        context = {"aluno": self.listaSessoes,
                   "dataEscolhida": request.GET.get('dataEscolhida',""),
                   'sessoes': sessoes}
        

        return render(request, 'TemplateGerenciamentoTreinos.html',context)
    
    def post(self, request,cpf):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")



        acao = request.POST.get('acao')
        match acao:
            case 'Excluir':
                self.alunoRepository.deletarAgendamento(cpf, request.POST.get('dia'))
                return redirect("gerenciamentoTreinos", cpf=cpf)

            case 'Salvar':
                agendamento = {
                    'cpf': cpf,
                    'dia': request.POST.get('dia'),
                    'exercicios': sequenciaTolista.strTolista(request.POST.get('exercicios')),
                    'idSessao': request.POST.get('idSessao'),
                }
                self.alunoRepository.atualizarAgendamento(agendamento)
                return redirect("gerenciamentoTreinos", cpf=cpf)

            case 'filtrar':
                try :
                    self.listaSessoes = self.alunoRepository.listarSessaoPorDia(cpf,request.POST.get('dataEscolhida'))
                except:
                    return redirect("gerenciamentoTreinos", cpf=cpf)


        for index, i in enumerate(self.listaSessoes.get('sessoes')):
            i["idSessao"] = index
            i['dia'] = i.get('dia').strftime("%Y-%m-%dT%H:%M")
            i['exerciciosList'] = ';\n'.join(i.get('exercicios'))

        self.listaSessoes["sessoes"] = sorted(self.listaSessoes["sessoes"], key=lambda k: k['dia'])

        p = Paginator(self.listaSessoes.get('sessoes'), 1)

        sessoes = p.get_page(1)

        context = {"aluno":self.listaSessoes,
                "dataEscolhida":request.POST.get('dataEscolhida'),
                   'sessoes': sessoes}

        return render(request, 'TemplateGerenciamentoTreinos.html',context)

        




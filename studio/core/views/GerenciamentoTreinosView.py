from time import strptime

from django.views import View
from django.shortcuts import render, redirect

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo

from core.services.sequenciaTolista import sequenciaTolista


class GerenciamentoTreinosView(View):
    def __init__(self):

        self.mongoClinte = ConexaoMongo()
        self.mongoClinte._colecao = self.mongoClinte._mydb["aluno"]

        self.alunoRepository = AlunoRepository(self.mongoClinte)

    def get(self,request,cpf):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        listaSessoes = self.alunoRepository.listarSessoes(cpf)
        
        for index, i in enumerate(listaSessoes.get('sessoes')):
            i["idSessao"] = index
            i['dia'] = i.get('dia').strftime("%Y-%m-%dT%H:%M")
            i['exerciciosList'] = ';\n'.join(i.get('exercicios'))
        context = {'listaSessoes':listaSessoes}
        

        return render(request, 'TemplateGerenciamentoTreinos.html',context)
    
    def post(self, request,cpf):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        agendamento = {
                        'cpf':cpf,
                        'dia':request.POST.get('dia'),
                        'exercicios': sequenciaTolista.strTolista(request.POST.get('exercicios')),
                        'idSessao': request.POST.get('idSessao'),
        }

        acao = request.POST.get('acao')
        match acao:
            case 'Excluir':
                self.alunoRepository.deletarAgendamento(agendamento)

            case 'Salvar':
                self.alunoRepository.atualizarAgendamento(agendamento)
        
        return redirect("gerenciamentoTreinos",cpf=cpf)



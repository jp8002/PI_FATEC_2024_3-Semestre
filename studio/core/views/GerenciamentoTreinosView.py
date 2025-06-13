from django.views import View
from django.shortcuts import render, redirect

from core.repositories.AlunoRepository import AlunoRepository
from core.services.Autenticar import Autenticar
from core.services.ConexaoMongo import ConexaoMongo
from datetime import datetime


class GerenciamentoTreinosView(View):
    def get(self,request,id):
        if not Autenticar.checarSessao(request.session):
            return redirect("paginaInicial")
        if not Autenticar.checarSessaoPersonal(request.session):
            return redirect("paginaInicial")

        mongoClinte = ConexaoMongo()
        mongoClinte._colecao = mongoClinte._mydb["aluno"]

        alunoRepository = AlunoRepository(mongoClinte)

        listaSessoes = alunoRepository.listarSessoes(id)
        
        for index, i in enumerate(listaSessoes.get('sessoes')):
            i["idSessao"] = index
            i['dia'] = i.get('dia').strftime("%Y-%m-%dT%H:%M")
            i['exerciciosList'] = ';\n'.join(i.get('exercicios'))
        context = {'listaSessoes':listaSessoes}
        

        return render(request, 'TemplateGerenciamentoTreinos.html',context)
    
    def post(self, request,id):
        
        print(request.POST , id)
        
        return redirect("paginaInicial")



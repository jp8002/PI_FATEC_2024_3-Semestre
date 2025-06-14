from django.views import View
from django.shortcuts import render, redirect
from core.services.ConexaoMongo import ConexaoMongo
from core.repositories.AlunoRepository import AlunoRepository


class DashboardView(View):
    def __init__(self):
        self.mongoClinte = ConexaoMongo()
        self.mongoClinte._colecao = self.mongoClinte._mydb["aluno"]
        self.alunoRepository = AlunoRepository(self.mongoClinte)

    def get(self,request):
        balancoAlunos = self.alunoRepository.TodosAlunosPorStatus().to_list()
        
        alunosPorPersonal = self.alunoRepository.TodosAlunosPorPersonal().to_list()
        for i in alunosPorPersonal:
            i["id"] = i.get("_id")
       
        context = {"balancoAlunos":balancoAlunos,
                    "alunosPorPersonal":alunosPorPersonal}

        return render(request, "TemplateTelaDashboard.html",context)


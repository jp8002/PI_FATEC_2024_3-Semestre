from django.shortcuts import render
import pymongo
import ipdb
from core.services import ServiceMongo
from core.services import Autenticar

# Create your views here.
def View_Pagina_Inicial(request):
    contexto={}
    #ipdb.set_trace()
    if request.session.get('Sessao',False) and request.session.get("ClienteID", False):
        ClienteID = request.session.get("ClienteID", False)
        serviceM = ServiceMongo()
       
        serviceM._colecao = serviceM._mydb["clientes"]
        
        cliente = serviceM.consultar(ClienteID)
        contexto={'cliente':cliente}
    
    return render(request, "TemplatePaginaInicial.html",contexto)
    
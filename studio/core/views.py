from django.shortcuts import render
from core.services import ServiceMongo

# Create your views here.
def View_Pagina_Inicial(request):
    service = ServiceMongo()
    x = service.consultar_datas_agendadas()

    return render(request, "TemplatePaginaInicial.html", {"x":x})
    pass
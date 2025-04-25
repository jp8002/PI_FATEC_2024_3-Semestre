from django.shortcuts import render
import ipdb

# Create your views here.
def View_Pagina_Inicial(request):
    
    #ipdb.set_trace()
    print(request.session["teste"])
    return render(request, "TemplatePaginaInicial.html")
    pass
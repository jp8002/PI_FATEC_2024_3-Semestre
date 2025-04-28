from django.urls import path
from . import views

urlpatterns = [
    path('', views.View_Pagina_Inicial, name="paginaInicial"),
    path('calendario/', views.Calendario, name="paginaCalendario")

]
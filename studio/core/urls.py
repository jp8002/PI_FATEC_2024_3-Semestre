from django.urls import path
from . import views

urlpatterns = [
    path('', views.View_Pagina_Inicial, name="paginaInicial"),
    path('calendario/', views.Calendario, name="paginaCalendario"),
    path('login/', views.View_Login, name='paginaLogin'),
    path('aluno/', views.View_AlunoInicial, name="alunoInicial"),
    path('cadastrarPersonal/', views.View_CadastrarPersonal, name="cadastrarPersonal"),
    path('personal/', views.View_PersonalInicial, name='personalInicial'),
    path('personal/cadastrar_personal', views.View_AlunoCadastrar, name='cadastrarAluno')
]
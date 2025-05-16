from django.urls import path
from . import views

urlpatterns = [
    path('', views.View_Pagina_Inicial, name="paginaInicial"),
    path('calendario/', views.Calendario, name="paginaCalendario"),
    path('login/', views.View_Login, name='paginaLogin'),
    path('aluno/', views.View_AlunoInicial, name="alunoInicial"),
    path('cadastrarPersonal/', views.View_CadastrarPersonal, name="cadastrarPersonal"),
    path('personal/', views.View_PersonalInicial, name='personalInicial'),
    path('personal/cadastrar_personal', views.View_CadastrarAluno, name='cadastrarAluno'),

    path("personal/agendar_treino", views.View_AgendarTreino, name='agendarTreino'),

    path("personal/deletar_agendamento", views.View_DeletarAgendamento, name='deletarAgendamento'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    path("personal/criar_treino", views.View_CriarTreinoAluno, name='criarTreino'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    path("personal/deletar_treino", views.View_DeletarTreinoAluno, name='deletarTreino'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    path("personal/atualizar_personal", views.View_AtualizarPersonal, name='atualizarPersonal'),
    
]
from django.urls import path
from .views.View_AgendarTreino import AgendarTreinoView
from .views.View_AlunoInicial import AlunoInicialView
from .views.View_AtualizarPersonal import AtualizarPersonalView
from .views.View_CadastrarAluno import CadastrarAlunoView
from .views.View_CadastrarPersonal import CadastrarPersonalView
from .views.View_Calendario import CalendarioViews
from .views.View_CriarTreinoAluno import CriarTreinoAlunoView
from .views.View_DeletarAgendamento import DeletarAgendamentoView
from .views.View_DeletarTreinoAluno import DeletarTreinoAlunoView
from .views.View_Login import LoginView
from .views.View_Pagina_Inicial import PaginaInicialView
from .views.View_PersonalInicial import PersonalInicialView

urlpatterns = [
    path('', PaginaInicialView.as_view(), name="paginaInicial"),
    path('calendario/', CalendarioViews.as_view(), name="paginaCalendario"),
    path('login/', LoginView.as_view(), name='paginaLogin'),
    path('aluno/', AlunoInicialView.as_view(), name="alunoInicial"),
    path('cadastrarPersonal/', CadastrarPersonalView.as_view(), name="cadastrarPersonal"),
    path('personal/', PersonalInicialView.as_view(), name='personalInicial'),
    path('personal/cadastrar_aluno', CadastrarAlunoView.as_view(), name='cadastrarAluno'),

    path("personal/agendar_treino", AgendarTreinoView.as_view(), name='agendarTreino'),

    path("personal/deletar_agendamento", DeletarAgendamentoView.as_view(), name='deletarAgendamento'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    path("personal/criar_treino", CriarTreinoAlunoView.as_view(), name='criarTreino'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    path("personal/deletar_treino", DeletarTreinoAlunoView.as_view(), name='deletarTreino'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    path("personal/atualizar_personal", AtualizarPersonalView.as_view(), name='atualizarPersonal'),
    
]
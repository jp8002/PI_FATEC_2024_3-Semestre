from django.urls import path

from .views.View_GerenciamentoAgendamentos import GerenciamentoAgendamentosView
from .views.View_AgendarTreino import AgendarTreinoView

#from .views.View_AtualizarPersonal import AtualizarPersonalView
from .views.View_CadastrarAluno import CadastrarAlunoView
from .views.View_CadastrarPersonal import CadastrarPersonalView
from .views.View_DeletarAgendamento import DeletarAgendamentoView

from .views.View_Login import LoginView
from .views.View_Pagina_Inicial import PaginaInicialView
from .views.View_PersonalInicial import PersonalInicialView
from .views.View_ListarAlunos import ListarAlunosView
from .views.View_ListarPersonal import ListarPersonalView
from .views.View_Dashboard import DashboardView
from .views.View_Sair import SairView
from .views.View_EditarAluno import EditarAlunoView
from .views.View_EditarPersonal import EditarPersonalView
from .views.View_AlunoPersonal import AlunoPersonalView

urlpatterns = [
    path('', PaginaInicialView.as_view(), name="paginaInicial"),
    path('login/', LoginView.as_view(), name='paginaLogin'),
    path('cadastrarPersonal/', CadastrarPersonalView.as_view(), name="cadastrarPersonal"),
    path('personal/', PersonalInicialView.as_view(), name='personalInicial'),
    path('personal/cadastrar_aluno', CadastrarAlunoView.as_view(), name='cadastrarAluno'),
    path('personal/editar_aluno/<str:cpf>/', EditarAlunoView.as_view(), name='editarAluno'),
    path('personal/editar_personal/<str:cpf>/', EditarPersonalView.as_view(), name='editarPersonal'),

    path('personal/gerenciamento_treinos/<str:cpf>', GerenciamentoAgendamentosView.as_view(), name='gerenciamentoAgendamentos'),

    path("personal/agendar_treino", AgendarTreinoView.as_view(), name='agendarTreino'),

    path("personal/deletar_agendamento", DeletarAgendamentoView.as_view(), name='deletarAgendamento'), #FIQUEI NA DUVIDA E DEIXEI EM VIEWS SEPARADAS ~KPO
    #path("personal/atualizar_personal", AtualizarPersonalView.as_view(), name='atualizarPersonal'),
    path("personal/listar_alunos", ListarAlunosView.as_view(), name='listarAlunos'),
    path("personal/listar_personal", ListarPersonalView.as_view(), name='listarPersonal'),
    path('personal/dashboard/', DashboardView.as_view(), name='dashboard'),

    path('personal/alunopersonal/<str:personal>/', AlunoPersonalView.as_view(), name='alunopersonal'),
    path("sair", SairView.as_view(), name="sair")
    
]
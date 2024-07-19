from django.urls import path
from .views import TarefaCreate, TarefaUpdate, TarefaDelete, TarefaList, concluir_tarefa

urlpatterns = [
    path('tarefa/cadastrar/', TarefaCreate.as_view(), name='cadastrar-tarefa'),
    path('tarefa/<int:pk>/editar/', TarefaUpdate.as_view(), name='editar-tarefa'),
    path('tarefa/<int:pk>/excluir/', TarefaDelete.as_view(), name='excluir-tarefa'),
    path('tarefas/', TarefaList.as_view(), name='listar-tarefas'),

    path('concluir-tarefa/', concluir_tarefa , name='concluir-tarefa'),
]

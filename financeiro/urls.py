from django.urls import path
from .views import MovimentacaoCreate, MovimentacaoList, MovimentacaoDelete
from .views import obter_dados_entrada, obter_dados_saida  
from . import views

urlpatterns = [
    path('movimentacao/nova/', MovimentacaoCreate.as_view(), name='cadastrar-movimentacao'),
    path('movimentacoes/', MovimentacaoList.as_view(), name='listar-movimentacoes'),
    path('movimentacao/excluir/<pk>/', MovimentacaoDelete.as_view(), name='excluir-movimentacao'),

    path('obter-dados-entrada/', obter_dados_entrada, name='obter-dados-entrada'),
    path('obter-dados-saida/', obter_dados_saida, name='obter-dados-saida'),
    path('tipo-movimentacao/', views.tipo_movimentacao, name='tipo-movimentacao'),
    path('grafico/', views.exibir_grafico, name='grafico'),
]

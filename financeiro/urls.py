from django.urls import path
from .views import SaidaCreate, SaidaDelete, SaidaList, EntradaCreate, EntradaDelete, EntradaList
from .views import obter_dados_entrada, obter_dados_saida  
from . import views

urlpatterns = [
    path('cadastrar/saida/', SaidaCreate.as_view(), name='cadastrar-saida'),
    path('excluir/movimentacao/<int:pk>/', SaidaDelete.as_view(), name='excluir-saida'),
    path('listar/movimentacao/', SaidaList.as_view(), name='listar-saida'),  
    path('cadastrar/entrada/', EntradaCreate.as_view(), name='cadastrar-entrada'),
    path('excluir/movimetacao/<int:pk>/', EntradaDelete.as_view(), name='excluir-entrada'),
    path('listar/movimentacao/', EntradaList.as_view(), name='listar-entrada'), 
    path('obter-dados-entrada/', obter_dados_entrada, name='obter-dados-entrada'),
    path('obter-dados-saida/', obter_dados_saida, name='obter-dados-saida'),
    path('tipo-movimentacao/', views.tipo_movimentacao, name='tipo-movimentacao'),
    path('grafico/', views.exibir_grafico, name='grafico'),
]

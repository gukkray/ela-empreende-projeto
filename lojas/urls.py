from django.urls import path, include
from . import views
from .views import (
    ComentarioCreate, ComentarioUpdate, ComentarioDelete, VendaDelete,
    buscar_produto, iniciar_venda, adicionar_produto, finalizar_venda, get_total_venda, listar_vendas, exibir_comentarios, buscar_produtos_por_loja
)

urlpatterns = [  
    path('cadastrar/comentario/', ComentarioCreate.as_view(), name='cadastrar-comentario'),
    path('editar/comentario/<int:pk>/', ComentarioUpdate.as_view(), name='editar-comentario'),
    path('excluir/comentario/<int:pk>/', ComentarioDelete.as_view(), name='excluir-comentario'),

    path('buscar-produto/', buscar_produto, name='buscar_produto'),
    path('iniciar-venda/', iniciar_venda, name='iniciar_venda'),
    path('adicionar-produto/<int:venda_id>/', views.adicionar_produto, name='adicionar_produto'),
    path('finalizar-venda/<int:venda_id>/', views.finalizar_venda, name='finalizar_venda'),
    path('excluir-venda/<int:pk>/', VendaDelete.as_view(), name='excluir_venda'),
    
    path('get-total-venda/<int:venda_id>/', get_total_venda, name='get_total_venda'),
    path('vendas/', listar_vendas, name='listar_vendas'),
    path('buscar-produtos-por-loja/', buscar_produtos_por_loja, name='buscar_produtos_por_loja'),
    path('select2/', include('django_select2.urls')),
    path('venda/<int:venda_id>/excluir-item/<int:item_id>/', views.excluir_item_venda, name='excluir_item_venda'),
    path('cadastrar/categoria/', views.CategoriaCreateView.as_view(), name='cadastrar_categoria'),
    path('comentarios/<int:categoria_id>/', views.exibir_comentarios, name='exibir_comentarios'),
    path('comentarios/', views.exibir_comentarios, name='exibir_comentarios_sem_categoria'),

]



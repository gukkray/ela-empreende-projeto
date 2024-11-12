from django.urls import path
from .views import ProdutoCreate, ProdutoUpdate, ProdutoDelete, ProdutoList, ProdutosGeraisList
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cadastrar/produto/', ProdutoCreate.as_view(), name='cadastrar-produto'),
    path('editar/produto/<int:pk>/', ProdutoUpdate.as_view(), name='editar-produto'),
    path('excluir/produto/<int:pk>/', ProdutoDelete.as_view(), name='excluir-produto'),
    path('listar/produto/', ProdutoList.as_view(), name='listar-produto'),
    path('produtos/gerais/', ProdutosGeraisList.as_view(), name='produtos_gerais'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

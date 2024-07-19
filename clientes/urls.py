# clientes/urls.py
from django.urls import path
from .views import ClienteCreate, ClienteUpdate, ClienteDeleteView, ClienteListView

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', ClienteCreate.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/', ClienteUpdate.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/excluir/', ClienteDeleteView.as_view(), name='cliente_delete'),
]

from django.urls import path
from .views import IndexView, ModeloView, InicioView, tarefas_json, minha_view, minha_view_de_logout

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('modelo/', ModeloView.as_view(), name='modelo'),
    path('inicio/', minha_view, name='inicio'),
    path('logout/', minha_view_de_logout, name='logout'),
    path('tarefas/json/', tarefas_json, name='tarefas_json'),
]

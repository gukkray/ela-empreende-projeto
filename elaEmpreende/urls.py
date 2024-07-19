# /home/jaqueline/elaEmpreende/elaEmpreende/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Paginas.urls')),
    path('', include('gerenciar.urls')),
    path('', include("usuarios.urls")),
    path('', include("lojas.urls")),
    path('', include("tarefas.urls")),
    path('', include("financeiro.urls")),
    path('', include("clientes.urls")),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


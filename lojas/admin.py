from django.contrib import admin
from .models import Comentario, Venda



class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'data_publicacao')  # Campos exibidos na lista de comentários


admin.site.register(Comentario)

admin.site.register(Venda)

# admin.py

from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')  # Coloque os campos que você deseja exibir
    search_fields = ('nome',)  # Permite pesquisar por nome no admin
    list_filter = ('nome',)  # Filtro para categorias no painel de administração


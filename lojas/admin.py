from django.contrib import admin
from .models import Comentario, Venda



class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'data_publicacao')  # Campos exibidos na lista de comentários


admin.site.register(Comentario)

admin.site.register(Venda)

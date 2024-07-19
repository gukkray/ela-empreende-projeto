# from django.contrib import admin
# from .models import Produto


# admin.site.register(Produto)

# class Produto(admin.ModelAdmin):
#     list_display = ["nome", "descricao", "preco", "quantidade_estoque", "portifolio", "imagem_produto"]

from django.contrib import admin
from .models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao", "preco", "quantidade_estoque", "imagem", 'na_loja']

admin.site.register(Produto, ProdutoAdmin)


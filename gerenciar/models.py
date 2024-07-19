from django.db import models
from django.conf import settings
from django.utils import timezone

class Produto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, null=False)
    descricao = models.TextField(null=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    quantidade_estoque = models.PositiveIntegerField(null=False)
    imagem = models.ImageField(verbose_name='Foto ilustrativa do produto', upload_to='fotos_produto', null=True, blank=True)
    na_loja = models.BooleanField(default=True, verbose_name='Disponível na loja', null=False)
    oferta = models.BooleanField(default=True, verbose_name='Produto em oferta', null=False)
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name='Data de criação')
    data_modificacao = models.DateTimeField(auto_now=True, verbose_name='Última modificação')
    

    def __str__(self):
        return self.nome 

    def aumentar_estoque(self, quantidade):
        self.quantidade_estoque += quantidade
        self.save()

    def diminuir_estoque(self, quantidade):
        if quantidade <= self.quantidade_estoque:
            self.quantidade_estoque -= quantidade
            self.save()
        else:
            raise ValueError("Quantidade insuficiente em estoque.")

    def atualizar_preco(self, novo_preco):
        self.preco = novo_preco
        self.save()

    


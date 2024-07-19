from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from gerenciar.models import Produto

class Venda(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name='Data de criação')
    data_modificacao = models.DateTimeField(auto_now=True, verbose_name='Última modificação')
    finalizado = models.BooleanField(default=False, verbose_name='Finalizado')  

    def save(self, *args, **kwargs):
        # Atualiza a data de criação apenas se a venda ainda não foi finalizada
        if not self.pk or not self.finalizado:
            self.data_criacao = timezone.now()
        super().save(*args, **kwargs)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(help_text="")
    data_publicacao = models.DateTimeField(auto_now_add=True)
    resposta_a = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respostas')

    def __str__(self):
        return f"Comentário por {self.autor.username} em {self.data_publicacao.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

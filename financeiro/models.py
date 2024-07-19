from django.db import models
from django.conf import settings
from django.utils import timezone


class Movimentacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField(null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    data = models.DateField(default=timezone.now, verbose_name='Data da movimentação')
    

    def __str__(self):
        return self.descricao

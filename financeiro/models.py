from django.db import models
from django.conf import settings
from django.utils import timezone

class Movimentacao(models.Model):
    TIPO_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField(null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    data = models.DateField(default=timezone.now, verbose_name='Data da movimentação')
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO, null=False, default='entrada')  # Campo de escolha

    def __str__(self):
        return f"{self.descricao} ({self.get_tipo_display()})"
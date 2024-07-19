from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tarefas')

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos')

class Venda(models.Model):
    pass


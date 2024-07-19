from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, blank=True)
    imagem = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Endereco(models.Model):
 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.endereco}, {self.cidade}, {self.estado}"

class Contato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contato = models.CharField(max_length=100, blank=True, null=True)
    contato2 = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.contato}"
    

class Links(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkswhatsapp = models.CharField(max_length=100, blank=True, null=True)
    linksfacebook = models.CharField(max_length=100, blank=True, null=True)
    linksinstagram = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.linksfacebook}, {self.linksinstagram}, {self.linkswhatsapp}"

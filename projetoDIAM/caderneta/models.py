from django.contrib.auth.models import User
from django.db import models
from django.forms import forms
from django.utils import timezone
from django.core.validators import MaxValueValidator


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.IntegerField(default=0)
    data_nascimento = models.DateField(null=True, blank=True)
    n_cromos = models.IntegerField(default=0)
    imagem = models.CharField(max_length=1000, default='/media/default_image.jpg')

    def __str__(self):
        return self.user.username

    def get_imagem_url(self):
        if self.imagem:
            return self.imagem
        else:
            return 'default_image.jpg'

class Mensagem(models.Model):
    user = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    mensagem_texto = models.CharField(max_length=300)
    n_likes = models.IntegerField(default=0)
    pub_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensagem_texto

class Like(models.Model):
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE)
    user = models.ForeignKey(Utilizador, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.username} liked {self.mensagem.id}"

class Pacote(models.Model):
    titulo = models.CharField(max_length=25)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    qnt_cromos = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    descricao = models.CharField(max_length=50)
    imagem = models.CharField(max_length=200, default='/caderneta/Images/Pacotes/default_Pacote.jpg')
    cromos = models.ManyToManyField('Cromo')

    def __str__(self):
        return self.titulo

class Cromo(models.Model):
    nome = models.CharField(max_length=30)
    posicao = models.CharField(max_length=30)
    imagem = models.CharField(max_length=200, default='/caderneta/Images/Fotos jogadores/default_Player.jpg')
    selecao = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Caderneta(models.Model):
    cromo = models.ForeignKey(Cromo, on_delete=models.CASCADE)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

class CromoPacote(models.Model):
    cromo = models.ForeignKey(Cromo, on_delete=models.CASCADE)
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
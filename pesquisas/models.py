import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Pergunta(models.Model):
  texto_pergunta = models.CharField(max_length=200)
  data_publicacao = models.DateTimeField('data da publicação')

  def __str__(self):
    return self.texto_pergunta

  def publicado_recentemente(self):
    return self.data_publicacao >= timezone.now() - datetime.timedelta(days=1)

class Opcao(models.Model):
  pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
  texto_opcao = models.CharField(max_length=200)
  votos = models.IntegerField(default=0)

  def __str__(self):
    return self.texto_opcao

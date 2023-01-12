from django.shortcuts import render
from django.http import HttpResponse
from .models import Pergunta

# Create your views here.

def inicio(pedido):
  ultimas_perguntas = Pergunta.objects.order_by('-data_publicacao'[:5])
  lista_perguntas = ', '.join([p.texto_pergunta for p in ultimas_perguntas])
  return HttpResponse(lista_perguntas)

def detalhe(pedido, pergunta_id):
  return HttpResponse("Você está vendo a pergunta %s." % pergunta_id)

def resultados(pedido, pergunta_id):
  resposta = "Você está vendo os resultados da pergunta %s."
  return HttpResponse(resposta % pergunta_id)

def votar(pedido, pergunta_id):
  return HttpResponse("Você está votando na pergunta %s." % pergunta_id)

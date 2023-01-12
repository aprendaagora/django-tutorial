from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Pergunta

# Create your views here.

def inicio(pedido):
  ultimas_perguntas = Pergunta.objects.order_by("-data_publicacao")[:5]
  contexto = {
    'ultimas_perguntas': ultimas_perguntas
  }
  return render(pedido, 'pesquisas/inicio.html', contexto)

def detalhes(pedido, pergunta_id):
  pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
  return render(pedido, 'pesquisas/detalhes.html', {'pergunta': pergunta})

def resultados(pedido, pergunta_id):
  resposta = "Você está vendo os resultados da pergunta %s."
  return HttpResponse(resposta % pergunta_id)

def votar(pedido, pergunta_id):
  return HttpResponse("Você está votando na pergunta %s." % pergunta_id)

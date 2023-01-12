from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Pergunta, Opcao

# Create your views here.

class RotaInicio(generic.ListView):
  template_name = 'pesquisas/inicio.html'
  context_object_name = 'ultimas_perguntas'

  def get_queryset(self):
    return Pergunta.objects.order_by('-data_publicacao')[:5]

class RotaDetalhes(generic.DetailView):
  model = Pergunta
  template_name = 'pesquisas/detalhes.html'

class RotaResultados(generic.DetailView):
  model = Pergunta
  template_name = 'pesquisas/resultados.html'

def votar(pedido, pergunta_id):
  pergunta = get_object_or_404(Pergunta, pk=pergunta_id)

  try:
    opcao_selecionada = pergunta.opcao_set.get(pk=pedido.POST['opcao'])
  except (KeyError, Opcao.DoesNotExist):
    return render(pedido, 'pesquisas/detalhes.html', {
      'pergunta': pergunta,
      'mensagem_erro': "Você não selecionou uma opção.",
    })
  else:
    opcao_selecionada.votos += 1
    opcao_selecionada.save()

    return HttpResponseRedirect(reverse('pesquisas:resultados', args=(pergunta.id,)))
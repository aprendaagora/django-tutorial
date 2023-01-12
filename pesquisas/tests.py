from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Pergunta

# Create your tests here.

def criar_pergunta(texto_pergunta, dias):
  data = timezone.now() + datetime.timedelta(days=dias)
  return Pergunta.objects.create(texto_pergunta=texto_pergunta, data_publicacao=data)

class PerguntaModelTests(TestCase):

  def test_nenhuma_pergunta(self):
    # resposta do servidor (não da pergunta)
    pagina = self.client.get(reverse('pesquisas:inicio'))
    self.assertEqual(pagina.status_code, 200)
    self.assertContains(pagina, "Não há perguntas.")
    self.assertQuerysetEqual(pagina.context['ultimas_perguntas'], [])

  def test_pergunta_no_passado(self):
    pergunta = criar_pergunta(texto_pergunta="Pergunta no passado.", dias=-30)
    pagina = self.client.get(reverse('pesquisas:inicio'))
    self.assertQuerysetEqual(
      pagina.context['ultimas_perguntas'],
      [pergunta]
    )

  def test_pergunta_no_futuro(self):
    criar_pergunta(texto_pergunta="Pergunta no futuro.", dias=30)
    pagina = self.client.get(reverse('pesquisas:inicio'))
    self.assertContains(pagina, "Não há perguntas.")
    self.assertQuerysetEqual(pagina.context['ultimas_perguntas'], [])
  
  def test_pergunta_no_futuro_e_pergunta_no_passado(self):
    pergunta_no_passado = criar_pergunta(texto_pergunta="Pergunta no passado.", dias=-30)
    criar_pergunta(texto_pergunta="Pergunta no futuro", dias=30)
    pagina = self.client.get(reverse('pesquisas:inicio'))
    self.assertQuerysetEqual(
      pagina.context['ultimas_perguntas'],
      [pergunta_no_passado]
    )
  
  def test_duas_perguntas_no_passado(self):
    pergunta1 = criar_pergunta(texto_pergunta="Pergunta 1", dias=-30)
    pergunta2 = criar_pergunta(texto_pergunta="Pergunta 2", dias=-5)
    pagina = self.client.get(reverse('pesquisas:inicio'))
    self.assertQuerysetEqual(
      pagina.context['ultimas_perguntas'],
      [pergunta2, pergunta1]
    )

  def test_publicado_recentemente_com_pergunta_no_futuro(self):
    data = timezone.now() + datetime.timedelta(days=30)
    pergunta_futura = Pergunta(data_publicacao=data)
    self.assertIs(pergunta_futura.publicado_recentemente(), False)

  def test_publicado_recentemente_com_pergunta_antiga(self):
    data = timezone.now() - datetime.timedelta(days=1, seconds=1)
    pergunta_antiga = Pergunta(data_publicacao=data)
    self.assertIs(pergunta_antiga.publicado_recentemente(), False)
  
  def test_publicado_recentemente_com_pergunta_recente(self):
    data = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    pergunta_recente = Pergunta(data_publicacao=data)
    self.assertIs(pergunta_recente.publicado_recentemente(), True)

class PerguntaRotaDetalhesTests(TestCase):
  def test_pergunta_no_futuro(self):
    pergunta_no_futuro = criar_pergunta(texto_pergunta="Pergunta no futuro.", dias=30)
    url = reverse('pesquisas:detalhes', args=(pergunta_no_futuro.id,))
    pagina = self.client.get(url)
    self.assertEqual(pagina.status_code, 404)

  def test_pergunta_no_passado(self):
    pergunta_no_passado = criar_pergunta(texto_pergunta="Pergunta no passado.", dias=-5)
    url = reverse('pesquisas:detalhes', args=(pergunta_no_passado.id,))
    pagina = self.client.get(url)
    self.assertContains(pagina, pergunta_no_passado.texto_pergunta)
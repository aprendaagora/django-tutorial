from django.urls import path

from . import views

app_name = 'pesquisas'
urlpatterns = [
  path('', views.inicio, name='inicio'),
  path('<int:pergunta_id>/', views.detalhes, name='detalhes'),
  path('<int:pergunta_id>/resultados/', views.resultados, name='resultados'),
  path('<int:pergunta_id>/votar/', views.votar, name='votar')
]
from django.urls import path

from . import views

app_name = 'pesquisas'
urlpatterns = [
  path('', views.RotaInicio.as_view(), name='inicio'),
  path('<int:pk>/', views.RotaDetalhes.as_view(), name='detalhes'),
  path('<int:pk>/resultados/', views.RotaResultados.as_view(), name='resultados'),
  path('<int:pergunta_id>/votar/', views.votar, name='votar')
]
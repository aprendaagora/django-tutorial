from django.contrib import admin

# Register your models here.

from .models import Pergunta, Opcao

class OpcaoInline(admin.TabularInline):
  model = Opcao
  extra = 3
  verbose_name = "Opção"
  verbose_name_plural = "Opções"

class PerguntaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['texto_pergunta']}),
    ('Informação da data', {'fields': ['data_publicacao'], 'classes': ['collapse']})
  ]
  inlines = [OpcaoInline]
  list_display = ('texto_pergunta', 'data_publicacao', 'publicado_recentemente')
  list_filter = ['data_publicacao']
  search_fields = ['texto_pergunta']


admin.site.register(Pergunta, PerguntaAdmin)

from django.contrib import admin
from .models import MentoriaContato


@admin.register(MentoriaContato)
class MentoriaContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    search_fields = ('nome', 'email')
    list_filter = ('criado_em',)
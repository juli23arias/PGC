from django.contrib import admin
from .models import NormaTransito


@admin.register(NormaTransito)
class NormaTransitoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'articulo', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo']
    search_fields = ['titulo', 'descripcion', 'articulo']

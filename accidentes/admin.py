from django.contrib import admin
from .models import Accidente


@admin.register(Accidente)
class AccidenteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'gravedad', 'ubicacion', 'fecha', 'reportado_por', 'activo']
    list_filter = ['gravedad', 'activo', 'fecha']
    search_fields = ['titulo', 'ubicacion', 'descripcion']
    date_hierarchy = 'fecha'

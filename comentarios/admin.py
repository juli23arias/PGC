from django.contrib import admin
from .models import Comentario, Like


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'accidente', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido', 'autor__username']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'comentario', 'fecha']

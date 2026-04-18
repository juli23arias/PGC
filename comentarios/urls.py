from django.urls import path
from . import views

app_name = 'comentarios'

urlpatterns = [
    path('accidente/<int:accidente_pk>/comentar/', views.agregar_comentario, name='agregar'),
    path('comentario/<int:comentario_pk>/like/', views.dar_like, name='like'),
    path('comentario/<int:pk>/eliminar/', views.eliminar_comentario, name='eliminar'),
]

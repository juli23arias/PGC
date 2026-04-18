from django.urls import path
from . import views

app_name = 'normas'

urlpatterns = [
    path('', views.lista_normas, name='lista'),
    path('norma/<int:pk>/', views.detalle_norma, name='detalle'),
    path('norma/nueva/', views.crear_norma, name='crear'),
    path('norma/<int:pk>/editar/', views.editar_norma, name='editar'),
    path('norma/<int:pk>/eliminar/', views.eliminar_norma, name='eliminar'),
]

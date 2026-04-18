from django.urls import path
from . import views

app_name = 'accidentes'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('ruta/', views.ruta_segura, name='ruta_segura'),
    path('mapa/datos/', views.mapa_json, name='mapa_json'),
    path('accidente/<int:pk>/', views.detalle_accidente, name='detalle'),
    path('accidente/nuevo/', views.crear_accidente, name='crear'),
    path('accidente/<int:pk>/editar/', views.editar_accidente, name='editar'),
    path('accidente/<int:pk>/eliminar/', views.eliminar_accidente, name='eliminar'),
]

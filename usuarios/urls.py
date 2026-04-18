from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    # Gestión de usuarios (solo admin)
    path('gestion/', views.lista_usuarios, name='lista_usuarios'),
    path('gestion/crear/', views.crear_usuario, name='crear_usuario'),
    path('gestion/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('gestion/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
]

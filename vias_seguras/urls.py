from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accidentes.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('comentarios/', include('comentarios.urls')),
    path('normas/', include('normas.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vias_seguras.settings')
django.setup()

from accidentes.models import Accidente

coords = {
    'Choque en intersección de Av. Caracas': (4.6240, -74.0777),
    'Motociclista herido en vía rápida':     (4.7568, -74.0407),
    'Raspón entre bus y automóvil':           (4.6361, -74.0649),
    'Accidente múltiple en Calle 80':         (4.6875, -74.0990),
    'Ciclista impactado por vehículo':        (4.6769, -74.1035),
    'Volcamiento de camión de carga':          (4.4500, -74.0200),
}

for titulo, (lat, lng) in coords.items():
    updated = Accidente.objects.filter(titulo__startswith=titulo[:30]).update(latitud=lat, longitud=lng)
    print(f"  {'OK' if updated else 'NO'} {titulo[:50]}")

print("Coordenadas actualizadas.")

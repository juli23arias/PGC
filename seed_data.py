import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vias_seguras.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil
from accidentes.models import Accidente
from comentarios.models import Comentario, Like
from normas.models import NormaTransito
from django.utils import timezone
from datetime import timedelta
import random

print("Creando datos de ejemplo...")

# Superusuario/admin
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@viasseguras.co', 'admin123')
    admin.first_name = 'Administrador'
    admin.last_name = 'Sistema'
    admin.save()
    Perfil.objects.get_or_create(
        usuario=admin,
        defaults={'rol': 'administrador'}
    )
    print("  Admin creado: admin / admin123")

# Usuarios de prueba
usuarios_data = [
    ('carlos123', 'Carlos', 'Mendoza', 'carlos@ejemplo.co'),
    ('maria_v', 'María', 'Vargas', 'maria@ejemplo.co'),
    ('juan_p', 'Juan', 'Pérez', 'juan@ejemplo.co'),
]
usuarios = []
for username, first, last, email in usuarios_data:
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, 'usuario123')
        u.first_name = first
        u.last_name = last
        u.save()
        if not hasattr(u, 'perfil'):
            Perfil.objects.create(usuario=u, rol='usuario')
        usuarios.append(u)
        print(f"  Usuario creado: {username} / usuario123")
    else:
        usuarios.append(User.objects.get(username=username))

admin_user = User.objects.get(username='admin')

# Accidentes
accidentes_data = [
    {
        'titulo': 'Choque en intersección de Av. Caracas',
        'ubicacion': 'Av. Caracas con Calle 26, Bogotá',
        'descripcion': 'Colisión entre dos vehículos particulares en la intersección. El semáforo presentó falla técnica momentos antes del accidente. Uno de los conductores resultó con heridas leves y fue atendido en el sitio por paramédicos del CRUE.',
        'gravedad': 'media',
        'fecha': timezone.now() - timedelta(days=2, hours=3),
        'reportado_por': usuarios[0] if usuarios else admin_user,
    },
    {
        'titulo': 'Motociclista herido en vía rápida',
        'ubicacion': 'Autopista Norte Km 15, Bogotá',
        'descripcion': 'Motociclista perdió el control del vehículo al esquivar un hueco en la vía. El accidentado fue trasladado al Hospital de Kennedy con fractura en la clavícula. Se reporta daño total de la motocicleta.',
        'gravedad': 'alta',
        'fecha': timezone.now() - timedelta(days=1, hours=7),
        'reportado_por': usuarios[1] if len(usuarios) > 1 else admin_user,
    },
    {
        'titulo': 'Raspón entre bus y automóvil',
        'ubicacion': 'Carrera 7 con Calle 45, Bogotá',
        'descripcion': 'Leve colisión entre un bus del SITP y un automóvil particular en horas pico. No se reportaron heridos. Los daños materiales son menores. El tráfico fue afectado por aproximadamente 20 minutos.',
        'gravedad': 'baja',
        'fecha': timezone.now() - timedelta(hours=5),
        'reportado_por': usuarios[2] if len(usuarios) > 2 else admin_user,
    },
    {
        'titulo': 'Accidente múltiple en Calle 80',
        'ubicacion': 'Calle 80 con Autopista Medellín, Bogotá',
        'descripcion': 'Accidente en cadena que involucró 4 vehículos en horas de la tarde. Dos personas fueron trasladadas al hospital con heridas de consideración. La vía estuvo bloqueada por más de 2 horas.',
        'gravedad': 'alta',
        'fecha': timezone.now() - timedelta(days=3),
        'reportado_por': admin_user,
    },
    {
        'titulo': 'Ciclista impactado por vehículo',
        'ubicacion': 'Ciclovía Av. El Dorado, Bogotá',
        'descripcion': 'Ciclista fue impactado por un vehículo que invadió la ciclovía. El ciclista presentó contusiones leves y fue trasladado a un centro de salud cercano para revisión.',
        'gravedad': 'media',
        'fecha': timezone.now() - timedelta(days=4),
        'reportado_por': usuarios[0] if usuarios else admin_user,
    },
    {
        'titulo': 'Volcamiento de camión de carga',
        'ubicacion': 'Vía Bogotá - Villavicencio Km 43',
        'descripcion': 'Camión de carga volcó en una curva pronunciada. El conductor sufrió heridas graves y fue trasladado en helicóptero. La mercancía (alimentos) quedó esparcida en la vía. Vía cerrada por 6 horas.',
        'gravedad': 'alta',
        'fecha': timezone.now() - timedelta(days=5),
        'reportado_por': admin_user,
    },
]

accidentes = []
for data in accidentes_data:
    if not Accidente.objects.filter(titulo=data['titulo']).exists():
        acc = Accidente.objects.create(**data)
        accidentes.append(acc)
        print(f"  Accidente: {acc.titulo[:50]}")
    else:
        accidentes.append(Accidente.objects.get(titulo=data['titulo']))

# Comentarios
comentarios_data = []
if accidentes and usuarios:
    comentarios_data = [
        (accidentes[0], usuarios[1] if len(usuarios)>1 else admin_user, "Pasé por ese sector esta mañana y efectivamente el semáforo sigue sin funcionar correctamente. Hay que reportarlo a la SDM."),
        (accidentes[0], usuarios[2] if len(usuarios)>2 else admin_user, "Es una intersección muy peligrosa. Se necesitan más agentes de tránsito en esa zona."),
        (accidentes[1], usuarios[0], "Es muy común ver motociclistas a alta velocidad en esa autopista. Necesitan más controles."),
        (accidentes[1], admin_user, "Hemos reportado el estado del pavimento a la Secretaría de Obras. Esperamos pronta respuesta."),
        (accidentes[2], usuarios[0], "Los conductores de bus muchas veces no respetan el carril. Hay que reforzar las multas."),
        (accidentes[3], usuarios[1] if len(usuarios)>1 else admin_user, "Fue un accidente terrible. Espero que los heridos se recuperen pronto."),
        (accidentes[4], usuarios[2] if len(usuarios)>2 else admin_user, "Las ciclovías necesitan mejor señalización y barreras de protección."),
    ]

comentarios_creados = []
for acc, autor, contenido in comentarios_data:
    if not Comentario.objects.filter(accidente=acc, autor=autor, contenido=contenido[:50]).exists():
        c = Comentario.objects.create(accidente=acc, autor=autor, contenido=contenido)
        comentarios_creados.append(c)
        print(f"  Comentario de {autor.username}")

# Likes
if comentarios_creados and usuarios:
    for c in comentarios_creados[:4]:
        for u in random.sample(usuarios[:min(len(usuarios), 3)], min(2, len(usuarios))):
            Like.objects.get_or_create(comentario=c, usuario=u)

# Normas de tránsito
normas_data = [
    {
        'titulo': 'Límite de velocidad en zona urbana',
        'descripcion': 'En zonas urbanas, la velocidad máxima permitida es de 50 km/h para vehículos de transporte individual y 40 km/h para vehículos de transporte público y de carga. En zonas escolares y residenciales, el límite se reduce a 30 km/h. El incumplimiento de esta norma genera multa de categoría D.',
        'categoria': 'velocidad',
        'articulo': 'Art. 106, Ley 769 de 2002',
    },
    {
        'titulo': 'Límite de alcohol en sangre para conductores',
        'descripcion': 'Está prohibido conducir con una concentración de alcohol en sangre igual o superior a 40 mg de etanol por 100 ml de sangre (0.04 g/dL). Para conductores de vehículos de servicio público o de carga, la concentración permitida es cero. El incumplimiento acarrea la suspensión de la licencia y multa de categoría E.',
        'categoria': 'alcoholemia',
        'articulo': 'Art. 152, Ley 769 de 2002',
    },
    {
        'titulo': 'Uso obligatorio del cinturón de seguridad',
        'descripcion': 'Todo conductor y pasajero de vehículo automotor está obligado a usar el cinturón de seguridad. Los menores de edad deben viajar en silla especial para niños ubicada en el asiento trasero. El incumplimiento genera inmovilización del vehículo y multa de categoría C.',
        'categoria': 'general',
        'articulo': 'Art. 82, Ley 769 de 2002',
    },
    {
        'titulo': 'Señal de PARE: obligación de detenerse',
        'descripcion': 'Al encontrar una señal de PARE, el conductor debe detener completamente el vehículo antes de la línea de detención o del borde de la calzada transversal. Solo podrá continuar cuando sea seguro hacerlo. Ignorar una señal de PARE constituye una infracción de categoría D.',
        'categoria': 'senales',
        'articulo': 'Art. 60, Ley 769 de 2002',
    },
    {
        'titulo': 'Prioridad a peatones en cebras',
        'descripcion': 'Los vehículos deben ceder el paso a los peatones en los cruces peatonales señalizados (pasos de cebra). El conductor debe reducir la velocidad al aproximarse a un cruce peatonal y detener el vehículo cuando haya peatones cruzando. Infracción de categoría D en caso de incumplimiento.',
        'categoria': 'peatones',
        'articulo': 'Art. 76, Ley 769 de 2002',
    },
    {
        'titulo': 'Casco obligatorio para motociclistas',
        'descripcion': 'El conductor y el acompañante de motocicleta están obligados a usar casco de seguridad homologado. El casco debe estar correctamente ajustado y abrochado. El incumplimiento genera inmovilización del vehículo y multa de categoría C. El casco debe ser certificado por el ICONTEC.',
        'categoria': 'motocicletas',
        'articulo': 'Art. 94, Ley 769 de 2002',
    },
    {
        'titulo': 'Documentos obligatorios para conducir',
        'descripcion': 'Para circular, el conductor debe portar: licencia de conducción vigente y apropiada para el vehículo, SOAT vigente, revisión técnico-mecánica vigente (para vehículos con más de 2 años de matrícula), y tarjeta de propiedad del vehículo. La falta de alguno de estos documentos genera multa de categoría D.',
        'categoria': 'documentos',
        'articulo': 'Art. 30, Ley 769 de 2002',
    },
    {
        'titulo': 'Uso del celular mientras conduce',
        'descripcion': 'Está completamente prohibido el uso de teléfonos celulares mientras se conduce, a menos que se utilicen dispositivos de manos libres. El incumplimiento genera multa de categoría D y 6 puntos deducibles de la licencia de conducción. Esta norma aplica también para el uso de audífonos.',
        'categoria': 'infracciones',
        'articulo': 'Art. 77, Ley 769 de 2002',
    },
    {
        'titulo': 'Límite de velocidad en carretera',
        'descripcion': 'En carreteras nacionales, la velocidad máxima para automóviles es de 100 km/h, para vehículos de servicio público 80 km/h, y para vehículos de carga 80 km/h. En tramos de doble calzada sin separador, el límite es de 80 km/h para todos los vehículos.',
        'categoria': 'velocidad',
        'articulo': 'Art. 106, Ley 769 de 2002',
    },
    {
        'titulo': 'Prohibición de estacionarse en zonas amarillas',
        'descripcion': 'Está prohibido estacionar en zonas señalizadas con línea amarilla, esquinas, intersecciones, pasos peatonales, frentes de estaciones de bomberos, hidrantes, zonas de discapacitados no autorizados, y carriles de transporte público. El vehículo será inmovilizado y se generará multa de categoría D.',
        'categoria': 'senales',
        'articulo': 'Art. 78, Ley 769 de 2002',
    },
    {
        'titulo': 'Obligación de dar prelación a vehículos de emergencia',
        'descripcion': 'Todo conductor debe ceder el paso a las ambulancias, carros de bomberos, policía y otros vehículos de emergencia cuando tengan encendidas sus sirenas y luces de emergencia. Se debe despejar el carril moviéndose hacia la derecha y deteniéndose si es necesario.',
        'categoria': 'general',
        'articulo': 'Art. 63, Ley 769 de 2002',
    },
    {
        'titulo': 'Señalización en caso de accidente',
        'descripcion': 'En caso de accidente, el conductor está obligado a señalizar el área del accidente para prevenir nuevos siniestros. Debe usar triángulos reflectivos o conos de seguridad ubicados a mínimo 50 metros antes del sitio del accidente. También debe prestar auxilio a los heridos y dar aviso a las autoridades.',
        'categoria': 'infracciones',
        'articulo': 'Art. 131, Ley 769 de 2002',
    },
]

for norma_data in normas_data:
    if not NormaTransito.objects.filter(titulo=norma_data['titulo']).exists():
        n = NormaTransito.objects.create(**norma_data)
        print(f"  Norma: {n.titulo[:50]}")

print("\n✓ Datos de ejemplo creados exitosamente!")
print("  Admin: admin / admin123")
print("  Usuarios: carlos123, maria_v, juan_p / usuario123")

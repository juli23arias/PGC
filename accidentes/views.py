import json
from datetime import date, timedelta
from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from .models import Accidente
from .forms import AccidenteForm


def ruta_segura(request):
    """Página de cálculo de rutas seguras."""
    return render(request, 'accidentes/ruta.html')


def estadisticas(request):
    """Página de estadísticas con datos JSON embebidos para las gráficas."""
    qs = Accidente.objects.filter(activo=True)
    total = qs.count()

    # Por gravedad
    por_gravedad = {g: 0 for g in ('baja', 'media', 'alta')}
    for row in qs.values('gravedad').annotate(n=Count('id')):
        por_gravedad[row['gravedad']] = row['n']

    # Por mes — últimos 12 meses
    hace_12 = date.today().replace(day=1) - timedelta(days=365)
    por_mes_qs = (
        qs.filter(fecha__gte=hace_12)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(n=Count('id'))
        .order_by('mes')
    )
    meses_labels, meses_data = [], []
    MESES_ES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    for row in por_mes_qs:
        meses_labels.append(f"{MESES_ES[row['mes'].month - 1]} {row['mes'].year}")
        meses_data.append(row['n'])

    # Por zona — primeras 30 chars de ubicacion (o todo si es corto)
    zonas_raw = defaultdict(int)
    for a in qs.values_list('ubicacion', flat=True):
        zona = (a or 'Sin ubicación')[:30].strip().rstrip(',').strip()
        zonas_raw[zona] += 1
    zonas_sorted = sorted(zonas_raw.items(), key=lambda x: x[1], reverse=True)[:10]
    zonas_labels = [z[0] for z in zonas_sorted]
    zonas_data   = [z[1] for z in zonas_sorted]

    # Últimos 5 accidentes
    recientes = list(qs.order_by('-fecha')[:5].values(
        'id', 'titulo', 'gravedad', 'ubicacion', 'fecha'
    ))
    for r in recientes:
        r['fecha_str'] = r['fecha'].strftime('%d/%m/%Y')

    # Día de la semana
    DIAS = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    por_dia = [0] * 7
    for a in qs.values_list('fecha', flat=True):
        por_dia[a.weekday()] += 1

    context = {
        'total': total,
        'total_alta': por_gravedad['alta'],
        'total_media': por_gravedad['media'],
        'total_baja': por_gravedad['baja'],
        'pct_alta':  round(por_gravedad['alta']  / total * 100) if total else 0,
        'pct_media': round(por_gravedad['media'] / total * 100) if total else 0,
        'pct_baja':  round(por_gravedad['baja']  / total * 100) if total else 0,
        'json_gravedad_data': json.dumps([por_gravedad['baja'], por_gravedad['media'], por_gravedad['alta']]),
        'json_meses_labels':  json.dumps(meses_labels),
        'json_meses_data':    json.dumps(meses_data),
        'json_zonas_labels':  json.dumps(zonas_labels),
        'json_zonas_data':    json.dumps(zonas_data),
        'json_dias_labels':   json.dumps(DIAS),
        'json_dias_data':     json.dumps(por_dia),
        'recientes': recientes,
    }
    return render(request, 'accidentes/estadisticas.html', context)


def dashboard(request):
    accidentes = Accidente.objects.filter(activo=True)

    busqueda = request.GET.get('q', '')
    gravedad_filtro = request.GET.get('gravedad', '')

    if busqueda:
        accidentes = accidentes.filter(
            Q(titulo__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if gravedad_filtro:
        accidentes = accidentes.filter(gravedad=gravedad_filtro)

    total = accidentes.count()
    total_baja = Accidente.objects.filter(activo=True, gravedad='baja').count()
    total_media = Accidente.objects.filter(activo=True, gravedad='media').count()
    total_alta = Accidente.objects.filter(activo=True, gravedad='alta').count()

    context = {
        'accidentes': accidentes,
        'busqueda': busqueda,
        'gravedad_filtro': gravedad_filtro,
        'total': total,
        'total_baja': total_baja,
        'total_media': total_media,
        'total_alta': total_alta,
    }
    return render(request, 'accidentes/dashboard.html', context)


def mapa_json(request):
    """API JSON: devuelve todos los accidentes activos con coordenadas para el mapa."""
    accidentes = Accidente.objects.filter(activo=True, latitud__isnull=False, longitud__isnull=False)
    data = []
    for a in accidentes:
        data.append({
            'id': a.pk,
            'titulo': a.titulo,
            'ubicacion': a.ubicacion,
            'descripcion': a.descripcion,
            'gravedad': a.gravedad,
            'gravedad_display': a.get_gravedad_display(),
            'color': a.get_gravedad_color_hex(),
            'fecha': a.fecha.strftime('%d/%m/%Y %H:%M'),
            'lat': a.latitud,
            'lng': a.longitud,
            'url': f'/accidente/{a.pk}/',
            'reportado_por': a.reportado_por.get_full_name() or a.reportado_por.username if a.reportado_por else 'Anónimo',
        })
    return JsonResponse({'accidentes': data})


def detalle_accidente(request, pk):
    accidente = get_object_or_404(Accidente, pk=pk, activo=True)
    comentarios = accidente.comentarios.all().order_by('fecha_creacion')

    likes_usuario = set()
    if request.user.is_authenticated:
        from comentarios.models import Like
        likes_usuario = set(
            Like.objects.filter(usuario=request.user, comentario__accidente=accidente).values_list('comentario_id', flat=True)
        )

    context = {
        'accidente': accidente,
        'comentarios': comentarios,
        'likes_usuario': likes_usuario,
    }
    return render(request, 'accidentes/detalle.html', context)


@login_required
def crear_accidente(request):
    if request.method == 'POST':
        form = AccidenteForm(request.POST)
        if form.is_valid():
            accidente = form.save(commit=False)
            accidente.reportado_por = request.user
            accidente.save()
            messages.success(request, 'Accidente registrado exitosamente.')
            return redirect('accidentes:detalle', pk=accidente.pk)
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = AccidenteForm()

    return render(request, 'accidentes/form.html', {'form': form, 'titulo': 'Registrar Accidente', 'accion': 'Guardar'})


@login_required
def editar_accidente(request, pk):
    accidente = get_object_or_404(Accidente, pk=pk)

    if not (request.user == accidente.reportado_por or
            (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador())):
        messages.error(request, 'No tienes permiso para editar este accidente.')
        return redirect('accidentes:detalle', pk=pk)

    if request.method == 'POST':
        form = AccidenteForm(request.POST, instance=accidente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accidente actualizado exitosamente.')
            return redirect('accidentes:detalle', pk=accidente.pk)
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = AccidenteForm(instance=accidente)

    return render(request, 'accidentes/form.html', {
        'form': form,
        'titulo': 'Editar Accidente',
        'accion': 'Actualizar',
        'accidente': accidente
    })


@login_required
def eliminar_accidente(request, pk):
    accidente = get_object_or_404(Accidente, pk=pk)

    if not (request.user == accidente.reportado_por or
            (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador())):
        messages.error(request, 'No tienes permiso para eliminar este accidente.')
        return redirect('accidentes:detalle', pk=pk)

    if request.method == 'POST':
        accidente.activo = False
        accidente.save()
        messages.success(request, 'Accidente eliminado exitosamente.')
        return redirect('accidentes:dashboard')

    return render(request, 'accidentes/confirmar_eliminar.html', {'accidente': accidente})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from accidentes.models import Accidente
from .models import Comentario, Like
from .forms import ComentarioForm


@login_required
def agregar_comentario(request, accidente_pk):
    accidente = get_object_or_404(Accidente, pk=accidente_pk, activo=True)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.accidente = accidente
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'No se pudo agregar el comentario.')
    
    return redirect('accidentes:detalle', pk=accidente_pk)


@login_required
def dar_like(request, comentario_pk):
    comentario = get_object_or_404(Comentario, pk=comentario_pk)
    
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(
            comentario=comentario,
            usuario=request.user
        )
        if not created:
            like.delete()
            accion = 'removido'
        else:
            accion = 'agregado'
        
        total = comentario.total_likes()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'accion': accion, 'total': total})
    
    return redirect('accidentes:detalle', pk=comentario.accidente.pk)


@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    accidente_pk = comentario.accidente.pk
    
    if request.user == comentario.autor or (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador()):
        if request.method == 'POST':
            comentario.delete()
            messages.success(request, 'Comentario eliminado.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este comentario.')
    
    return redirect('accidentes:detalle', pk=accidente_pk)

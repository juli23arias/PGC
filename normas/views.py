from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import NormaTransito
from .forms import NormaForm


def lista_normas(request):
    normas = NormaTransito.objects.filter(activo=True)
    
    busqueda = request.GET.get('q', '')
    categoria_filtro = request.GET.get('categoria', '')
    
    if busqueda:
        normas = normas.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(articulo__icontains=busqueda)
        )
    
    if categoria_filtro:
        normas = normas.filter(categoria=categoria_filtro)
    
    categorias = NormaTransito.CATEGORIAS
    
    context = {
        'normas': normas,
        'busqueda': busqueda,
        'categoria_filtro': categoria_filtro,
        'categorias': categorias,
        'total': normas.count(),
    }
    return render(request, 'normas/lista.html', context)


def detalle_norma(request, pk):
    norma = get_object_or_404(NormaTransito, pk=pk, activo=True)
    return render(request, 'normas/detalle.html', {'norma': norma})


@login_required
def crear_norma(request):
    if not (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador()):
        messages.error(request, 'Solo los administradores pueden crear normas.')
        return redirect('normas:lista')
    
    if request.method == 'POST':
        form = NormaForm(request.POST)
        if form.is_valid():
            norma = form.save()
            messages.success(request, 'Norma creada exitosamente.')
            return redirect('normas:detalle', pk=norma.pk)
    else:
        form = NormaForm()
    
    return render(request, 'normas/form.html', {'form': form, 'titulo': 'Nueva Norma', 'accion': 'Guardar'})


@login_required
def editar_norma(request, pk):
    if not (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador()):
        messages.error(request, 'Solo los administradores pueden editar normas.')
        return redirect('normas:lista')
    
    norma = get_object_or_404(NormaTransito, pk=pk)
    
    if request.method == 'POST':
        form = NormaForm(request.POST, instance=norma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Norma actualizada exitosamente.')
            return redirect('normas:detalle', pk=norma.pk)
    else:
        form = NormaForm(instance=norma)
    
    return render(request, 'normas/form.html', {'form': form, 'titulo': 'Editar Norma', 'accion': 'Actualizar', 'norma': norma})


@login_required
def eliminar_norma(request, pk):
    if not (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador()):
        messages.error(request, 'Solo los administradores pueden eliminar normas.')
        return redirect('normas:lista')
    
    norma = get_object_or_404(NormaTransito, pk=pk)
    
    if request.method == 'POST':
        norma.activo = False
        norma.save()
        messages.success(request, 'Norma eliminada.')
        return redirect('normas:lista')
    
    return render(request, 'normas/confirmar_eliminar.html', {'norma': norma})

"""Vistas del módulo de usuarios: autenticación y gestión de usuarios (solo admin)."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistroForm, LoginForm
from .models import Perfil
from django.http import HttpResponse

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def solo_admin(request):
    """Devuelve True si el usuario es administrador."""
    return (
        request.user.is_authenticated
        and hasattr(request.user, 'perfil')
        and request.user.perfil.es_administrador()
    )


def requiere_admin(request):
    """Muestra error y redirige si el usuario no es admin."""
    messages.error(request, 'Acceso denegado. Solo los administradores pueden realizar esta acción.')
    return redirect('accidentes:dashboard')


# ──────────────────────────────────────────────────────────────
# Autenticación
# ──────────────────────────────────────────────────────────────

def debug_admin(request):
    u = User.objects.get(username='admin')
    return HttpResponse(f"is_staff={u.is_staff}, is_superuser={u.is_superuser}")

def registro(request):
    if request.user.is_authenticated:
        return redirect('accidentes:dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user, rol='usuario')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'¡Bienvenido, {user.first_name or user.username}! Tu cuenta ha sido creada.')
            return redirect('accidentes:dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accidentes:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})


# ──────────────────────────────────────────────────────────────
# Gestión de usuarios — solo administradores
# ──────────────────────────────────────────────────────────────
@login_required
def lista_usuarios(request):
    if not solo_admin(request):
        return requiere_admin(request)

    usuarios = User.objects.select_related('perfil').all().order_by('date_joined')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


@login_required
def crear_usuario(request):
    if not solo_admin(request):
        return requiere_admin(request)

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol = request.POST.get('rol', 'usuario')
            Perfil.objects.create(usuario=user, rol=rol)
            messages.success(request, f'Usuario "{user.username}" creado correctamente.')
            return redirect('usuarios:lista_usuarios')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/form_usuario.html', {
        'form': form,
        'titulo': 'Crear Usuario',
        'accion': 'Crear',
    })


@login_required
def editar_usuario(request, pk):
    if not solo_admin(request):
        return requiere_admin(request)

    usuario = get_object_or_404(User, pk=pk)
    perfil_obj, _ = Perfil.objects.get_or_create(usuario=usuario, defaults={'rol': 'usuario'})

    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name', '').strip()
        usuario.last_name  = request.POST.get('last_name', '').strip()
        usuario.email      = request.POST.get('email', '').strip()
        usuario.save()
        perfil_obj.rol = request.POST.get('rol', 'usuario')
        perfil_obj.save()
        messages.success(request, f'Usuario "{usuario.username}" actualizado.')
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/editar_usuario.html', {
        'usuario': usuario,
        'perfil': perfil_obj,
    })


@login_required
def eliminar_usuario(request, pk):
    if not solo_admin(request):
        return requiere_admin(request)

    usuario = get_object_or_404(User, pk=pk)

    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('usuarios:lista_usuarios')

    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado correctamente.')
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/confirmar_eliminar_usuario.html', {'usuario': usuario})

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import Perfil


class Command(BaseCommand):
    help = 'Crear usuarios iniciales (admin y usuario) con perfil'

    def handle(self, *args, **kwargs):

        # ======================
        # ADMIN
        # ======================
        admin_user, _ = User.objects.update_or_create(
            username='admin',
            defaults={
                'email': 'admin@correo.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )

        # 🔥 Siempre asegurar contraseña
        admin_user.set_password('admin123')
        admin_user.save()

        self.stdout.write(self.style.SUCCESS('✔ Admin creado/actualizado'))

        Perfil.objects.get_or_create(
            usuario=admin_user,
            defaults={'rol': 'administrador'}
        )
        Perfil.objects.update_or_create(
            usuario=admin_user,
            defaults={'rol': 'administrador'}
        )

        # ======================
        # USUARIO NORMAL
        # ======================
        normal_user, _ = User.objects.update_or_create(
            username='usuario',
            defaults={
                'email': 'user@correo.com',
                'is_staff': False,
                'is_superuser': False,
            }
        )

        # 🔥 Siempre asegurar contraseña
        normal_user.set_password('user123')
        normal_user.save()

        self.stdout.write(self.style.SUCCESS('✔ Usuario creado/actualizado'))

        Perfil.objects.get_or_create(
            usuario=normal_user,
            defaults={'rol': 'usuario'}
        )

        self.stdout.write(self.style.SUCCESS('🔥 Seed ejecutado correctamente'))
        self.stdout.write(f"Admin staff: {admin_user.is_staff}")
        self.stdout.write(f"Admin superuser: {admin_user.is_superuser}")
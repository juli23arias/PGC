from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import Perfil


class Command(BaseCommand):
    help = 'Crear usuarios iniciales (admin y usuario) con perfil'

    def handle(self, *args, **kwargs):

        # ======================
        # ADMIN
        # ======================
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@correo.com'
            }
        )

        # 🔥 SIEMPRE asegurar configuración del admin
        admin_user.email = 'admin@correo.com'
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        if created:
            self.stdout.write(self.style.SUCCESS('✔ Admin creado'))
        else:
            self.stdout.write(self.style.SUCCESS('✔ Admin actualizado'))

        Perfil.objects.get_or_create(
            usuario=admin_user,
            defaults={'rol': 'administrador'}
        )

        # ======================
        # USUARIO NORMAL
        # ======================
        normal_user, created = User.objects.get_or_create(
            username='usuario',
            defaults={
                'email': 'user@correo.com'
            }
        )

        # 🔥 SIEMPRE asegurar configuración del usuario
        normal_user.email = 'user@correo.com'
        normal_user.set_password('user123')
        normal_user.is_staff = False
        normal_user.is_superuser = False
        normal_user.save()

        if created:
            self.stdout.write(self.style.SUCCESS('✔ Usuario creado'))
        else:
            self.stdout.write(self.style.SUCCESS('✔ Usuario actualizado'))

        Perfil.objects.get_or_create(
            usuario=normal_user,
            defaults={'rol': 'usuario'}
        )

        self.stdout.write(self.style.SUCCESS('🔥 Seed ejecutado correctamente'))
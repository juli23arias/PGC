from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import Perfil

class Command(BaseCommand):
    help = 'Crear usuarios iniciales (admin y usuario) con perfil'

    def handle(self, *args, **kwargs):

        # ======================
        # ADMIN
        # ======================
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@correo.com',
                password='admin123'
            )
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()

            Perfil.objects.create(
                usuario=admin_user,
                rol='administrador'
            )

            self.stdout.write(self.style.SUCCESS('✔ Admin creado con perfil'))
        else:
            self.stdout.write('Admin ya existe')

        # ======================
        # USUARIO NORMAL
        # ======================
        if not User.objects.filter(username='usuario').exists():
            normal_user = User.objects.create_user(
                username='usuario',
                email='user@correo.com',
                password='user123'
            )
            normal_user.save()

            Perfil.objects.create(
                usuario=normal_user,
                rol='usuario'
            )

            self.stdout.write(self.style.SUCCESS('✔ Usuario creado con perfil'))
        else:
            self.stdout.write('Usuario ya existe')

        self.stdout.write(self.style.SUCCESS('🔥 Seed ejecutado correctamente'))
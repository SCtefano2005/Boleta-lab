from django.core.management.base import BaseCommand
from empresa.models import Empleado

class Command(BaseCommand):
    help = 'Seed database with Empleados'

    def handle(self, *args, **kwargs):
        # Definir empleados
        empleados = [
            {'nombre': 'Juan', 'apellidos': 'Pérez López', 'dni': '12345678'},
            {'nombre': 'María', 'apellidos': 'García Sánchez', 'dni': '87654321'},
            {'nombre': 'Carlos', 'apellidos': 'Fernández Ruiz', 'dni': '11223344'},
            {'nombre': 'Ana', 'apellidos': 'Martínez Gómez', 'dni': '44332211'},
        ]

        # Crear empleados
        for emp_data in empleados:
            empleado, created = Empleado.objects.get_or_create(
                nombre=emp_data['nombre'],
                apellidos=emp_data['apellidos'],
                dni=emp_data['dni']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Empleado '{empleado.nombre} {empleado.apellidos}' creado satisfactoriamente"))
            else:
                self.stdout.write(f"Empleado con DNI {empleado.dni} ya existe")

from django.core.management.base import BaseCommand
from clientes.models import Cliente, Ciudad, Departamento, Provincia

class Command(BaseCommand):
    help = 'Crea clientes de prueba en la base de datos'

    def handle(self, *args, **kwargs):
        # Asegúrate de que las entidades relacionadas existan
        departamento = Departamento.objects.create(nombre='Lima')
        provincia = Provincia.objects.create(nombre='Lima', departamento=departamento)
        ciudad = Ciudad.objects.create(nombre='Lima', provincia=provincia)

        # Crear clientes
        clientes_data = [
            {
                'nombres': 'Stefano',
                'apellidos': 'Villalva',
                'email': 'stefano@gmail.com',
                'direccion': ciudad,
                'ruc': '12345678901',
                'password': '123',
            },
            {
                'nombres': 'Erick',
                'apellidos': 'Galindo',
                'email': 'galindo@gmail.com',
                'direccion': ciudad,
                'ruc': '12345678902',
                'password': '123',
            },
            {
                'nombres': 'Fabio',
                'apellidos': 'Ochoa',
                'email': 'ochoa@gmail.com',
                'direccion': ciudad,
                'ruc': '12345678903',
                'password': '125',
            },
        ]

        for cliente_data in clientes_data:
            cliente = Cliente(
                nombres=cliente_data['nombres'],
                apellidos=cliente_data['apellidos'],
                email=cliente_data['email'],
                direccion=cliente_data['direccion'],
                ruc=cliente_data['ruc'],
            )
            cliente.set_password(cliente_data['password'])  # Establece la contraseña
            cliente.save()

        self.stdout.write(self.style.SUCCESS('Clientes de prueba creados con éxito.'))

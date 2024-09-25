from django.core.management.base import BaseCommand
from ventas.models import Producto, Categoria

class Command(BaseCommand):
    help = 'Seed database with simple products'

    def handle(self, *args, **kwargs):
        # Crear algunas categorías básicas
        categoria1, created = Categoria.objects.get_or_create(nombre='Electrónica', descripcion='Productos electrónicos')
        categoria2, created = Categoria.objects.get_or_create(nombre='Hogar', descripcion='Artículos para el hogar')

        # Definir productos simples
        productos = [
            {'nombre': 'Televisor', 'descripcion': 'Televisor 4K de 50 pulgadas', 'precio': 1500.00, 'categoria': categoria1},
            {'nombre': 'Refrigeradora', 'descripcion': 'Refrigeradora de dos puertas', 'precio': 2000.00, 'categoria': categoria2},
            {'nombre': 'Laptop', 'descripcion': 'Laptop de 14 pulgadas, Intel i7', 'precio': 3500.00, 'categoria': categoria1},
            {'nombre': 'Sofá', 'descripcion': 'Sofá de 3 plazas', 'precio': 1200.00, 'categoria': categoria2},
        ]

        # Crear los productos
        for prod_data in productos:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                descripcion=prod_data['descripcion'],
                precio=prod_data['precio'],
                categoria=prod_data['categoria']
            )
            self.stdout.write(self.style.SUCCESS(f"Producto '{producto.nombre}' creado satisfactoriamente"))

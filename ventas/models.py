from django.db import models
from clientes.models import Cliente
from empresa.models import Empleado
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cancelado = models.BooleanField(default=False)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_totales(self):
        detalles = self.detalles.all()  # Cambiar a 'detalles' que es el related_name
        subtotal = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
        igv = subtotal * Decimal(0.18)  # Calcular IGV (18%)
        total = subtotal + igv  # Total es subtotal más IGV
        return subtotal, igv, total

    def save(self, *args, **kwargs):
        # Guardar primero la factura para obtener un ID
        super().save(*args, **kwargs)
        
        # Calcular totales después de que la factura ha sido guardada
        self.subtotal, self.igv, self.total = self.calcular_totales()
        # Guardar nuevamente la factura con los totales
        super().save(update_fields=['subtotal', 'igv', 'total'])

    def __str__(self):
        return f"Factura {self.id} - Cliente: {self.cliente.nombres}"


class Detalle(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de factura {self.factura.id} - Producto: {self.producto.nombre}"

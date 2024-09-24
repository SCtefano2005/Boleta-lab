from django.db import models
from clientes.models import Cliente
from empresa.models import Empleado

class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nombre}, {self.descripcion}"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
    igv = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cancelado = models.BooleanField(default=False)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)  # ForeignKey to Empleado

    def __str__(self):
        return f"Factura {self.id} - Cliente: {self.cliente.nombres}"

class Detalle(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Renamed to 'producto'
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)     # Renamed to 'factura'
    cantidad = models.PositiveIntegerField(default=1)                  # Example of additional field
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Example of another field

    def __str__(self):
        return f"Detalle de factura {self.factura.id} - Producto: {self.producto.nombre}"


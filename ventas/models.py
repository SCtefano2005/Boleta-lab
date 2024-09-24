from django.db import models
from clientes.models import Cliente, Empresa

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
    igv = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cancelado = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.id} - Cliente: {self.cliente.nombres}"

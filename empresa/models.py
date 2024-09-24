from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    dni = models.CharField(max_length=8, unique=True)    
    
    def __str__(self):
        return {self.nombre, self.apellidos, self.dni}

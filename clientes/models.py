from django.db import models

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.ForeignKey(Ciudad, on_delete=models.CASCADE)  
    ruc = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    ruc = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre



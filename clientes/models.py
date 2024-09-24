from django.db import models
import hashlib

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
    email = models.EmailField(max_length=255, unique=True)
    direccion = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    ruc = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Almacenar la contraseña hasheada
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        """Hashea la contraseña y la guarda en el modelo."""
        self.password = self.hash_password(raw_password)

    @staticmethod
    def hash_password(raw_password):
        """Crea un hash SHA-256 para la contraseña."""
        return hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return self.password == Cliente.hash_password(raw_password)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


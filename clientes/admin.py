from django.contrib import admin
from .models import Cliente, Provincia, Departamento, Ciudad

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'email','password', 'ruc', 'direccion', 'is_active')
    search_fields = ('nombres', 'apellidos', 'email', 'ruc')
    ordering = ('email',)
    list_per_page = 30
    



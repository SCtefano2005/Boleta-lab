from django.contrib import admin
from django import forms
from .models import Factura, Detalle, Producto
from decimal import Decimal

class DetalleInline(admin.TabularInline):
    model = Detalle
    extra = 1  

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'empleado']  

    def clean(self):
        cleaned_data = super().clean()
        detalles = self.data.getlist('detalles-0-producto')  
        total_subtotal = Decimal('0.00')

        for i in range(len(detalles)):
            precio_unitario = Decimal(self.data.get(f'detalles-{i}-precio_unitario', 0))
            cantidad = Decimal(self.data.get(f'detalles-{i}-cantidad', 0))
            total_subtotal += precio_unitario * cantidad

        igv = total_subtotal * Decimal('0.18')  
        total = total_subtotal + igv  

        cleaned_data['subtotal'] = total_subtotal
        cleaned_data['igv'] = igv
        cleaned_data['total'] = total

        return cleaned_data

class FacturaAdmin(admin.ModelAdmin):
    form = FacturaForm
    inlines = [DetalleInline]
    readonly_fields = ('subtotal', 'igv', 'total')
    list_display = (
        'cliente', 'cliente_ruc', 'cliente_direccion', 
        'empleado', 'cancelado', 'subtotal', 'igv', 
        'total', 'detalle_productos', 'detalle_cantidad_total'
    )
    search_fields = ('cliente__nombres', 'empleado__nombre')

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.subtotal = form.cleaned_data['subtotal']
        obj.igv = form.cleaned_data['igv']
        obj.total = form.cleaned_data['total']
        obj.save()
    
    def detalle_productos(self, obj): # este da los detalles
        productos = obj.detalles.all()  
        return ", ".join([detalle.producto.nombre for detalle in productos])  

    def detalle_cantidad_total(self, obj): #este da el total
        detalles = obj.detalles.all()
        return sum([detalle.cantidad for detalle in detalles])  
    
     # Método para mostrar el RUC del cliente
    def cliente_ruc(self, obj):
        return obj.cliente.ruc

    # Método para mostrar la dirección del cliente
    def cliente_direccion(self, obj):
        return obj.cliente.direccion

    cliente_ruc.short_description = 'RUC del Cliente'
    cliente_direccion.short_description = 'Dirección del Cliente'
    detalle_productos.short_description = 'Productos'
    detalle_cantidad_total.short_description = 'Cantidad Total'

@admin.register(Detalle)
class DetalleAdmin(admin.ModelAdmin):
    list_display = ('producto__nombre', 'factura__id', 'cantidad', 'precio_unitario')
    search_fields = ('producto__nombre', 'factura__id')
    ordering = ('factura__id',)
    list_per_page = 30


admin.site.register(Factura, FacturaAdmin)
admin.site.register(Producto)  

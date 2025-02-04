from django.contrib import admin
from .models import Pedido, Factura, Producto, PagoStripe, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha', 'estado', 'total', 'menu')  # Añadir menu a list_display
    list_filter = ('estado', 'fecha')
    inlines = [ItemPedidoInline]
    search_fields = ('numero', 'cliente__nombre')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'pedido', 'total', 'fecha')
    readonly_fields = ('subtotal', 'impuestos', 'descuento', 'total')
    search_fields = ('numero', 'pedido__numero')

    def save_model(self, request, obj, form, change):
        obj.calcular_total()
        super().save_model(request, obj, form, change)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponibilidad')
    search_fields = ('nombre', 'descripcion')

@admin.register(PagoStripe)
class PagoStripeAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'factura', 'monto', 'fecha')
    readonly_fields = ('fecha',)
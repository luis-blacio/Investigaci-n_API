from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from pedidos.models import Pedido  # Importar el modelo Pedido
from menus.models import Menu  # Importar el modelo Menu


class Impuesto(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje = models.FloatField(validators=[MinValueValidator(0.0)])
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.porcentaje}%"


class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    cedula = models.CharField(max_length=20, unique=True)
    correo = models.EmailField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"


class Cliente(Persona):
    pass


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField(validators=[MinValueValidator(0.0)])
    descripcion = models.TextField()
    impuestos = models.ManyToManyField(Impuesto, blank=True)

    @cached_property
    def precio_con_impuestos(self):
        return self.precio * (1 + sum(imp.porcentaje for imp in self.impuestos.all()) / 100)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    numero = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='facturacion_pedidos')  # Relación con Menu

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Pedido #{self.numero}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.FloatField(validators=[MinValueValidator(0.0)])

    @cached_property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"


class Factura(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    metodo_pago = GenericForeignKey('content_type', 'object_id')

    numero = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)  # Relación con Pedido
    subtotal = models.FloatField(default=0.0)
    impuestos = models.FloatField(default=0.0)
    descuento = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    def calcular_total(self):
        self.subtotal = self.pedido.total
        self.impuestos = self.subtotal * 0.12  # Ejemplo IVA 12%
        self.total = self.subtotal + self.impuestos - self.descuento
        self.save()

    def __str__(self):
        return f"Factura #{self.numero}"


class PagoStripe(models.Model):
    factura = models.OneToOneField(Factura, on_delete=models.CASCADE, related_name='pago_stripe')
    payment_id = models.CharField(max_length=100, unique=True)
    monto = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago Stripe #{self.payment_id}"
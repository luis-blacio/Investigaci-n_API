from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from menus.models import Menu  # Importar el modelo Menu

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField(validators=[MinValueValidator(0.0)])
    descripcion = models.TextField()
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()

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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
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

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
import stripe
from .models import Factura, PagoStripe, Pedido

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    pedidos = Pedido.objects.all()
    return render(request, "Home.html", {'pedidos': pedidos})

@csrf_protect
@login_required
def create_checkout_session(request, pedido_id):
    try:
        pedido = Pedido.objects.get(pk=pedido_id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Pedido #{pedido.numero}'},
                    'unit_amount': int(pedido.total * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/facturacion/exito/?session_id={{CHECKOUT_SESSION_ID}}'),
            cancel_url=request.build_absolute_uri(f'/facturacion/cancelar/'),
        )
        return JsonResponse({'session_id': session.id})
    except Exception as e:
        return HttpResponseServerError(str(e))

@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            pedido = Pedido.objects.get(numero=session.metadata.get('pedido_id'))

            # Crear Factura
            factura = Factura.objects.create(
                pedido=pedido,
                subtotal=pedido.total,
                impuestos=pedido.total * 0.12,
                total=pedido.total * 1.12
            )

            # Registrar pago
            PagoStripe.objects.create(
                factura=factura,
                payment_id=session.payment_intent,
                monto=session.amount_total / 100
            )

            return render(request, "pagos.html", {
                'factura': factura,
                'pago': factura.pago_stripe
            })
        except Exception as e:
            return HttpResponseServerError(str(e))
    return redirect('facturacion:lista_pedidos')

@login_required
def payment_cancel(request):
    return render(request, "pagos_cancel.html")

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

def nuevo_pedido(request):
    # Lógica para crear nuevo pedido
    return render(request, 'nuevo_pedido.html')

def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    return render(request, 'detalle_pedido.html', {'pedido': pedido})

def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'lista_facturas.html', {'facturas': facturas})

def detalle_factura(request, factura_id):
    factura = Factura.objects.get(pk=factura_id)
    return render(request, 'detalle_factura.html', {'factura': factura})
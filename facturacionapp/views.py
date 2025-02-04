from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
import stripe
from .models import Factura, PagoStripe, Pedido

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, "Home.html")

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
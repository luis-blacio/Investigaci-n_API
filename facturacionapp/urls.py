# facturacionapp/urls.py
from django.urls import path
from facturacionapp import views

app_name = 'facturacion'

urlpatterns = [
    path('', views.home, name='home'),
    path('pedido/', views.lista_pedidos, name='lista_pedidos'),
    path('pedido/nuevo/', views.nuevo_pedido, name='nuevo_pedido'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('factura/', views.lista_facturas, name='lista_facturas'),
    path('factura/<int:factura_id>/', views.detalle_factura, name='detalle_factura'),
    path('crear/<int:pedido_id>/', views.create_checkout_session, name='crear_pago'),
    path('exito/', views.payment_success, name='pago_exito'),
    path('cancelar/', views.payment_cancel, name='pago_cancelado'),
]

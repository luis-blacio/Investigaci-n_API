from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.index, name='index'),
    # Añade aquí otras rutas necesarias para la aplicación 'pedidos'
]
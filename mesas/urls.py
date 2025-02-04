from django.urls import path
from . import views

app_name = 'mesas'

urlpatterns = [
    path('', views.index, name='index'),
    # Añade aquí otras rutas necesarias para la aplicación 'mesas'
]
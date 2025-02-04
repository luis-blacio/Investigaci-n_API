from django.contrib import admin
from django.urls import path, include
from facturacionapp import views as facturacion_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventario/', include('inventario.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('menus/', include('menus.urls')),
    path('mesas/', include('mesas.urls')),
    path('estadisticas/', include('estadisticas.urls')),
    path('', include('facturacionapp.urls')),
    path('mapa/', facturacion_views.mapa, name='mapa'),  # Nueva ruta para el mapa
]
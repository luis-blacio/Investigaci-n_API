from django.test import TestCase, Client
from django.urls import reverse
from .models import Pedido, Cliente


class PagosTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Cliente Test",
            cedula="1234567890",
            correo="test@example.com",
            direccion="Dirección Test",
            telefono="0999999999"
        )
        self.pedido = Pedido.objects.create(cliente=self.cliente)

    def test_pago_flow(self):
        client = Client()
        response = client.post(reverse('crear_pago', args=[self.pedido.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('session_id', response.json())
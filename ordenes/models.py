from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto

class Orden(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    direccion_envio = models.TextField()
    metodo_pago = models.CharField(max_length=50, default='efectivo')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Orden {self.id} - {self.usuario.username}'

class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.precio * self.cantidad

class Pago(models.Model):
    METODOS = [
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('efectivo', 'Efectivo'),
    ]
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=50, choices=METODOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='pendiente')
    numero_tarjeta = models.CharField(max_length=4, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pago {self.id} - {self.metodo}'
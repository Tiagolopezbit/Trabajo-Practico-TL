from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username}'

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f'{self.producto.nombre} x{self.cantidad}'
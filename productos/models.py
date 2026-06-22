from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, blank=True)
    stock = models.IntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Variante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    talla = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.producto.nombre} - {self.talla} - {self.color}'

class Resena(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reseña de {self.usuario.username} - {self.producto.nombre}'
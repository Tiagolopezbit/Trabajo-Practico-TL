from django.db import models

class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=[('porcentaje', 'Porcentaje'), ('fijo', 'Fijo')], default='porcentaje')
    activo = models.BooleanField(default=True)
    fecha_expiracion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.codigo
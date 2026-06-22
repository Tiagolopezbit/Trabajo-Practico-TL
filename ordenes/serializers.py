from rest_framework import serializers
from .models import Orden, ItemOrden, Pago
from productos.serializers import ProductoSerializer
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email']

class ItemOrdenSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemOrden
        fields = ['id', 'producto', 'cantidad', 'precio', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class OrdenSerializer(serializers.ModelSerializer):
    items = ItemOrdenSerializer(many=True, read_only=True)
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Orden
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
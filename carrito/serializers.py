from rest_framework import serializers
from .models import Carrito, ItemCarrito
from productos.serializers import ProductoSerializer

class ItemCarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'items', 'total']

    def get_total(self, obj):
        return obj.total()
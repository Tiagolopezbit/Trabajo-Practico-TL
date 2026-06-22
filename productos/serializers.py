from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Producto, Variante, Resena

class VarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    variantes = VarianteSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = '__all__'
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Carrito, ItemCarrito
from productos.models import Producto
from .serializers import CarritoSerializer

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return Response(CarritoSerializer(carrito).data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agregar_carrito(request):
    try:
        producto = Producto.objects.get(pk=request.data.get('productoId'))
    except Producto.DoesNotExist:
        return Response({'message': 'Producto no encontrado'}, status=404)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += int(request.data.get('cantidad', 1))
    else:
        item.cantidad = int(request.data.get('cantidad', 1))
    item.save()
    return Response(CarritoSerializer(carrito).data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def quitar_carrito(request, producto_id):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        item = ItemCarrito.objects.get(carrito=carrito, producto_id=producto_id)
        item.delete()
        return Response(CarritoSerializer(carrito).data)
    except Exception:
        return Response({'message': 'Error al quitar producto'}, status=400)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Producto, Variante, Resena
from .serializers import ProductoSerializer, VarianteSerializer, ResenaSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def productos(request):
    if request.method == 'GET':
        lista = Producto.objects.all()
        return Response(ProductoSerializer(lista, many=True).data)
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def producto_detalle(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response({'message': 'Producto no encontrado'}, status=404)

    if request.method == 'GET':
        return Response(ProductoSerializer(producto).data)
    if request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    producto.delete()
    return Response({'message': 'Producto eliminado ✅'})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def variantes(request, producto_id):
    try:
        producto = Producto.objects.get(pk=producto_id)
    except Producto.DoesNotExist:
        return Response({'message': 'Producto no encontrado'}, status=404)

    if request.method == 'GET':
        lista = Variante.objects.filter(producto=producto)
        return Response(VarianteSerializer(lista, many=True).data)

    serializer = VarianteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(producto=producto)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def resenas(request, producto_id):
    if request.method == 'GET':
        lista = Resena.objects.filter(producto_id=producto_id)
        return Response(ResenaSerializer(lista, many=True).data)
    serializer = ResenaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(usuario=request.user, producto_id=producto_id)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
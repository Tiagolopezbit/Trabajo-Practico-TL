from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Producto, Carrito, ItemCarrito, Orden, ItemOrden, Resena, Cupon, Pago
from .serializers import (ProductoSerializer, CarritoSerializer, OrdenSerializer,
                          ResenaSerializer, CuponSerializer, PagoSerializer, RegistroSerializer)

# ── AUTH ──────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Usuario registrado ✅', 'token': token.key}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'usuario': {'id': user.id, 'nombre': user.first_name, 'username': user.username, 'email': user.email}
        })
    return Response({'message': 'Credenciales incorrectas'}, status=400)

# ── PRODUCTOS ─────────────────────────────────────────────────────────────────

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

# ── CARRITO ───────────────────────────────────────────────────────────────────

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

# ── ORDENES ───────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ordenes(request):
    if request.method == 'GET':
        lista = Orden.objects.filter(usuario=request.user)
        return Response(OrdenSerializer(lista, many=True).data)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito or not carrito.items.exists():
        return Response({'message': 'El carrito está vacío'}, status=400)

    orden = Orden.objects.create(
        usuario=request.user,
        total=carrito.total(),
        direccion_envio=request.data.get('direccionEnvio', ''),
        metodo_pago=request.data.get('metodoPago', 'efectivo')
    )

    for item in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )
        item.producto.stock -= item.cantidad
        item.producto.save()

    carrito.items.all().delete()
    return Response(OrdenSerializer(orden).data, status=201)

# ── PAGOS ─────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def procesar_pago(request, orden_id):
    try:
        orden = Orden.objects.get(pk=orden_id, usuario=request.user)
    except Orden.DoesNotExist:
        return Response({'message': 'Orden no encontrada'}, status=404)

    metodo = request.data.get('metodo')
    numero_tarjeta = request.data.get('numero_tarjeta', '')

    if metodo in ['tarjeta_credito', 'tarjeta_debito'] and len(numero_tarjeta) < 4:
        return Response({'message': 'Número de tarjeta inválido'}, status=400)

    pago = Pago.objects.create(
        orden=orden,
        metodo=metodo,
        monto=orden.total,
        estado='aprobado',
        numero_tarjeta=numero_tarjeta[-4:] if numero_tarjeta else ''
    )

    orden.estado = 'pagado'
    orden.save()

    return Response({
        'message': 'Pago procesado exitosamente ✅',
        'pago': PagoSerializer(pago).data
    })

# ── RESEÑAS ───────────────────────────────────────────────────────────────────

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

# ── CUPONES ───────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def validar_cupon(request, codigo):
    try:
        cupon = Cupon.objects.get(codigo=codigo, activo=True)
        return Response({'descuento': cupon.descuento, 'tipo': cupon.tipo})
    except Cupon.DoesNotExist:
        return Response({'message': 'Cupón no válido'}, status=404)
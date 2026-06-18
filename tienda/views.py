from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
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

# ── FACTURA PDF ───────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def generar_factura(request, orden_id):
    try:
        orden = Orden.objects.get(pk=orden_id)
    except Orden.DoesNotExist:
        return Response({'message': 'Orden no encontrada'}, status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura-orden-{orden_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Encabezado
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 60, "GOTTI STORE")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 85, "Factura de compra")

    # Línea
    p.line(50, height - 100, width - 50, height - 100)

    # Datos de la orden
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 130, f"Orden N: {orden.id}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 150, f"Cliente: {orden.usuario.first_name} {orden.usuario.username}")
    p.drawString(50, height - 170, f"Email: {orden.usuario.email}")
    p.drawString(50, height - 190, f"Fecha: {orden.creado.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(50, height - 210, f"Direccion: {orden.direccion_envio}")
    p.drawString(50, height - 230, f"Metodo de pago: {orden.metodo_pago}")
    p.drawString(50, height - 250, f"Estado: {orden.estado.upper()}")

    # Línea
    p.line(50, height - 265, width - 50, height - 265)

    # Productos
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 285, "PRODUCTOS:")
    p.drawString(350, height - 285, "PRECIO")
    p.drawString(450, height - 285, "CANT.")
    p.drawString(510, height - 285, "SUBTOTAL")
    p.line(50, height - 295, width - 50, height - 295)

    y = height - 315
    p.setFont("Helvetica", 11)
    for item in orden.items.all():
        p.drawString(50, y, item.producto.nombre[:40])
        p.drawString(350, y, f"G. {int(item.precio):,}")
        p.drawString(450, y, str(item.cantidad))
        p.drawString(510, y, f"G. {int(item.subtotal()):,}")
        y -= 25

    # Total
    p.line(50, y - 10, width - 50, y - 10)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(350, y - 35, f"TOTAL: G. {int(orden.total):,}")

    # Pie de página
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, "2026 GOTTI Store - Todos los derechos reservados")

    p.showPage()
    p.save()

    return response
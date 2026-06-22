from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Orden, ItemOrden, Pago
from .serializers import OrdenSerializer, PagoSerializer
from carrito.models import Carrito

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

    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 60, "GOTTI STORE")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 85, "Factura de compra")
    p.line(50, height - 100, width - 50, height - 100)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 130, f"Orden N: {orden.id}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 150, f"Cliente: {orden.usuario.first_name} {orden.usuario.username}")
    p.drawString(50, height - 170, f"Email: {orden.usuario.email}")
    p.drawString(50, height - 190, f"Fecha: {orden.creado.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(50, height - 210, f"Direccion: {orden.direccion_envio}")
    p.drawString(50, height - 230, f"Metodo de pago: {orden.metodo_pago}")
    p.drawString(50, height - 250, f"Estado: {orden.estado.upper()}")
    p.line(50, height - 265, width - 50, height - 265)

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

    p.line(50, y - 10, width - 50, y - 10)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(350, y - 35, f"TOTAL: G. {int(orden.total):,}")
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, "2026 GOTTI Store - Todos los derechos reservados")

    p.showPage()
    p.save()
    return response
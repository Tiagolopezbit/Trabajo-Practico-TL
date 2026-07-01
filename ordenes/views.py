from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .models import Orden, ItemOrden, Pago
from .serializers import OrdenSerializer, PagoSerializer
from carrito.models import Carrito
import os

# Registrar fuente gótica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(BASE_DIR, 'MedievalSharp.ttf')
try:
    pdfmetrics.registerFont(TTFont('Gotica', FONT_PATH))
    GOTICA_DISPONIBLE = True
except:
    GOTICA_DISPONIBLE = False

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

    # ── LOGO GOTTI CON FUENTE GÓTICA ─────────────────────────────
    p.setFillColor(colors.black)
    p.rect(40, height - 95, 200, 75, fill=1, stroke=0)

    p.setFillColor(colors.white)
    if GOTICA_DISPONIBLE:
        p.setFont("Gotica", 42)
    else:
        p.setFont("Helvetica-Bold", 38)
    p.drawString(52, height - 58, "GOTTI")

    # Línea dorada decorativa
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.setLineWidth(3)
    p.line(40, height - 70, 240, height - 70)

    p.setFillColor(colors.white)
    p.setFont("Helvetica", 10)
    p.drawString(78, height - 85, "S  T  O  R  E")

    # ── INFO EMPRESA ─────────────────────────────────────────────
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 10)
    p.drawString(260, height - 50, "GOTTI Store")
    p.drawString(260, height - 63, "Asuncion, Paraguay")
    p.drawString(260, height - 76, "contacto@gotti.com.py")

    p.setFont("Helvetica-Bold", 18)
    p.drawString(420, height - 58, "FACTURA")
    p.setFont("Helvetica", 11)
    p.drawString(420, height - 75, f"N° {str(orden_id).zfill(6)}")

    # ── LÍNEA SEPARADORA ─────────────────────────────────────────
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(40, height - 108, width - 40, height - 108)

    # ── DATOS DE LA ORDEN ────────────────────────────────────────
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, height - 130, "DATOS DEL CLIENTE:")
    p.setFont("Helvetica", 11)
    p.drawString(40, height - 148, f"Cliente: {orden.usuario.first_name} {orden.usuario.username}")
    p.drawString(40, height - 164, f"Email: {orden.usuario.email}")
    p.drawString(40, height - 180, f"Direccion: {orden.direccion_envio}")

    p.setFont("Helvetica-Bold", 11)
    p.drawString(350, height - 130, "DETALLES:")
    p.setFont("Helvetica", 11)
    p.drawString(350, height - 148, f"Fecha: {orden.creado.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(350, height - 164, f"Metodo de pago: {orden.metodo_pago}")
    p.drawString(350, height - 180, f"Estado: {orden.estado.upper()}")

    # ── TABLA DE PRODUCTOS ───────────────────────────────────────
    p.line(40, height - 200, width - 40, height - 200)

    p.setFillColor(colors.black)
    p.rect(40, height - 225, width - 80, 22, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, height - 218, "PRODUCTO")
    p.drawString(320, height - 218, "PRECIO UNIT.")
    p.drawString(430, height - 218, "CANT.")
    p.drawString(490, height - 218, "SUBTOTAL")

    p.setFillColor(colors.black)
    y = height - 240
    for i, item in enumerate(orden.items.all()):
        if i % 2 == 0:
            p.setFillColor(colors.HexColor('#f5f5f5'))
            p.rect(40, y - 5, width - 80, 20, fill=1, stroke=0)
        p.setFillColor(colors.black)
        p.setFont("Helvetica", 10)
        p.drawString(50, y, item.producto.nombre[:35])
        p.drawString(320, y, f"G. {int(item.precio):,}")
        p.drawString(440, y, str(item.cantidad))
        p.drawString(490, y, f"G. {int(item.subtotal()):,}")
        y -= 22

    # ── TOTAL ────────────────────────────────────────────────────
    p.setLineWidth(1)
    p.line(40, y - 10, width - 40, y - 10)
    p.setFillColor(colors.black)
    p.rect(380, y - 40, width - 420, 25, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 13)
    p.drawString(390, y - 30, f"TOTAL: G. {int(orden.total):,}")

    # ── PIE DE PÁGINA ────────────────────────────────────────────
    p.setFillColor(colors.black)
    p.rect(40, 30, width - 80, 35, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 9)
    p.drawString(50, 52, "Gracias por tu compra en GOTTI Store")
    p.drawString(50, 40, "© 2026 GOTTI Store — Todos los derechos reservados — Asuncion, Paraguay")

    p.showPage()
    p.save()
    return response
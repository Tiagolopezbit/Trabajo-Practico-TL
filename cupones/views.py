from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Cupon
from .serializers import CuponSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def validar_cupon(request, codigo):
    try:
        cupon = Cupon.objects.get(codigo=codigo, activo=True)
        return Response({'descuento': cupon.descuento, 'tipo': cupon.tipo})
    except Cupon.DoesNotExist:
        return Response({'message': 'Cupón no válido'}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def crear_cupon(request):
    serializer = CuponSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
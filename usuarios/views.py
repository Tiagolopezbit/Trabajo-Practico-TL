from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')

    if User.objects.filter(username=username).exists():
        return Response({'message': 'El usuario ya existe'}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name
    )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'message': 'Usuario registrado ✅', 'token': token.key}, status=201)

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
            'usuario': {
                'id': user.id,
                'nombre': user.first_name,
                'username': user.username,
                'email': user.email
            }
        })
    return Response({'message': 'Credenciales incorrectas'}, status=400)
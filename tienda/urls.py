from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('api/auth/registro/', views.registro),
    path('api/auth/login/', views.login),

    # Productos
    path('api/productos/', views.productos),
    path('api/productos/<int:pk>/', views.producto_detalle),

    # Carrito
    path('api/carrito/', views.ver_carrito),
    path('api/carrito/agregar/', views.agregar_carrito),
    path('api/carrito/<int:producto_id>/', views.quitar_carrito),

    # Ordenes
    path('api/ordenes/', views.ordenes),

    # Pagos
    path('api/pagos/<int:orden_id>/', views.procesar_pago),

    # Reseñas
    path('api/resenas/<int:producto_id>/', views.resenas),

    # Cupones
    path('api/cupones/<str:codigo>/', views.validar_cupon),
]
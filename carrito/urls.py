from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito),
    path('agregar/', views.agregar_carrito),
    path('<int:producto_id>/', views.quitar_carrito),
]

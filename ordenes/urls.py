from django.urls import path
from . import views

urlpatterns = [
    path('', views.ordenes),
    path('pagos/<int:orden_id>/', views.procesar_pago),
    path('facturas/<int:orden_id>/', views.generar_factura),
    path('<int:orden_id>/', views.generar_factura),
]
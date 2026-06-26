from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos),
    path('<int:pk>/', views.producto_detalle),
    path('<int:producto_id>/variantes/', views.variantes),
    path('<int:producto_id>/resenas/', views.resenas),
]

from django.urls import path
from . import views

urlpatterns = [
    path('<str:codigo>/', views.validar_cupon),
    path('crear/', views.crear_cupon),
]